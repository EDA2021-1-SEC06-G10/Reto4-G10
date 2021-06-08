"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.ADT.indexminpq import size
from math import dist
from sys import path
import time
from DISClib.DataStructures.adjlist import addEdge
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import edge as edge
import DISClib.Algorithms.Graphs.dfs as depth
import DISClib.Algorithms.Graphs.dijsktra as djk
import DISClib.Algorithms.Graphs.prim as prim
import DISClib.Algorithms.Graphs.scc as scc
import DISClib.Algorithms.Graphs.dfo as dfo
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.Utils import error as error
import haversine as hs
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initialize():
    """ Inicializa el analizador:
            stops: Tabla de hash para guardar los vertices del grafo.
            connections: Grafo para representar las rutas entre estaciones.
            components: Almacena la informacion de los componentes conectados.
            paths: Estructura que almacena los caminos de costo minimo desde un
                   vértice determinado a todos los otros vértices del grafo.
    """
    try:
        analyzer = {
                    'countries': None,
                    'connections': None,
                    'components': None,
                    'paths': None,
                    'mst': None,
                    'dfs': None,
                    'info_lp': None,
                    'nombres_lp':None, 
                    'info_cables': None,
                    'nodos_capitales': None,
                    "check":None
                    }

        analyzer['countries'] = mp.newMap(numelements=250,
                                     maptype='PROBING',
                                     comparefunction=compareCountry)
        analyzer['info_cables']= mp.newMap(numelements=6000,
                                     maptype='PROBING',
                                     comparefunction=compareCountry)
        analyzer['nombres_lp']= mp.newMap(numelements=4000,
                                     maptype='PROBING',
                                     comparefunction=compareCountry)

        analyzer['info_lp']= mp.newMap(numelements=4000,
                                     maptype='PROBING',
                                     comparefunction=compareCountry)
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=6000,
                                              comparefunction=compareLPids)
        analyzer['nodos_capitales']= lt.newList("ARRAY_LIST")
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model.newAnalyzer')

# ===============================================
# Funciones para agregar información al catalogo
# ===============================================

def addCountry(catalog, country):
    lista= catalog['nodos_capitales']
    grafo= catalog['connections']
    paises= catalog['countries']
    name= country['CountryName'].lower()
    if name != "":
        entry=newCountry(country)
        mp.put(paises,name, entry)
        vert_cap= country['CapitalName'].lower()+'*'+name
        existscap= gr.containsVertex(grafo, vert_cap)
        if existscap==False:
            gr.insertVertex(grafo,vert_cap)
            lt.addLast(lista,vert_cap)

def newCountry(country):
    retorno={}
    retorno['infopais']=country
    retorno['nodos_asoc']=lt.newList()
    return retorno

def newLP(lp):
    retorno={}
    retorno["lp"]=lp
    retorno['LPsC']=mp.newMap(numelements=75,
                                     maptype='PROBING',
                                     comparefunction=compareCountry)
    retorno['cables']=mp.newMap(numelements=75,
                                     maptype='PROBING',
                                     comparefunction=compareCountry)
    return retorno

def addlp(catalog, info, nodo):
    lp_data= catalog['info_lp']
    name_info= catalog['nombres_lp']
    elLp=newLP(info)
    mp.put(lp_data, nodo, elLp)
    nombre=info['name'].lower()
    mp.put(name_info,nombre,nodo)


def samelp(grafo):
    list_vert= gr.vertices(grafo)
    i=0
    tamano= lt.size(list_vert)
    while i< tamano:
        elemento= lt.getElement(list_vert,i)
        corte=elemento.split('-')
        lp=corte[0]
        j=0
        k=0
        while j<tamano:
            elemento2=lt.getElement(list_vert,j)
            if elemento2!= elemento and (lp in elemento2):
                addEdges(grafo, elemento, elemento2,.100)
            j+=1
        i+=1

def addVertexescomp(catalog, link):
    try:
        grafo= catalog['connections']
        lpo=link['origin']
        origin=formatVertex(link, lpo)
        lpd= link['destination']
        destination=formatVertex(link,lpd)
        weight= link['cable_length']
        exists_origin=gr.containsVertex(grafo,origin)
        exists_destin= gr.containsVertex(grafo, destination)
        addcableInfo(link,catalog)
        addConnectingLP(origin, destination, catalog, link)
        addConnectingLP(destination, origin, catalog, link)
        addCabletoLp(destination, catalog)
        addCabletoLp(origin, catalog)
        if exists_origin==False:
            gr.insertVertex(grafo, origin)
            pais=findLPtoCountry(catalog,origin)
            addLPtoCountry(pais, origin, catalog)
            
        if exists_destin== False:
            gr.insertVertex(grafo, destination)
            pais=findLPtoCountry(catalog,destination)
            addLPtoCountry(pais, destination, catalog)
            
        addEdges(grafo, origin, destination,weight)
        return catalog
        
    except Exception as exp:
        error.reraise(exp, 'model:addVertexescomp')

def addEdges(grafo, origin, destination, weight):
    edge= gr.getEdge(grafo, origin, destination)
    if edge is None:
        gr.addEdge(grafo, origin, destination, weight)

def findLPtoCountry(catalog,origin):
    lps= catalog['info_lp']
    pre= origin.split("-")
    lpO=pre[0]
    entry=mp.get(lps,lpO)
    if entry!= None:
        minidic= me.getValue(entry)
        InfoLp= minidic["lp"]
        pre2=InfoLp['name'].split(", ")
        pais_lp= pre2[(len(pre2)-1)]

    return pais_lp.lower()

def findCountry(catalog,lp):
    lps= catalog['info_lp']
    entry=mp.get(lps,lp)
    if entry!= None:
        minidic= me.getValue(entry)
        InfoLp= minidic["lp"]
        pre2=InfoLp['name'].split(", ")
        pais_lp= pre2[1]
    return pais_lp.lower()

def addConnectingLP(lp1, lp2, catalog, link):
    landing_points=catalog['info_lp']
    pre= lp1.split("-")
    lpO= pre[0]
    pre2= lp2.split('-')
    lpD=pre2[0]
    entry=mp.get(landing_points,lpO)
    if entry!= None:
        minidic= me.getValue(entry)
        InfoLp= minidic["LPsC"]
        distancia=link['cable_length']
        mp.put(InfoLp, lpD, distancia)

def addCabletoLp(lp,catalog):
    landing_points=catalog['info_lp']
    pre= lp.split("-")
    lpO= pre[0]
    lista= pre[1:]
    cable= '-'.join(lista)
    entry=mp.get(landing_points,lpO)
    if entry!= None:
        minidic= me.getValue(entry)
        InfoLp= minidic["cables"]
        mp.put(InfoLp, cable, None)

def addLPtoCountry(pais, origin, catalog):
    paises=catalog['countries']
    entry=mp.get(paises, pais)
    if entry != None:
        minidic=me.getValue(entry)
        lista=minidic['nodos_asoc']
        lt.addLast(lista, origin)

def addcableInfo(link, catalog):
    nombre= link['cable_id']
    info_cables= catalog['info_cables']
    existe_cable=mp.contains(info_cables, nombre)
    if existe_cable==False:
        mp.put(info_cables,nombre,link)

def connectCLP(catalog):
    i=0
    mapalp=catalog['info_lp']
    grafo=catalog['connections']
    listaCLP= catalog['nodos_capitales']
    tamano = lt.size(listaCLP)
    mapa_paises= catalog['countries']
    while i <tamano:
        nodo_capital= lt.getElement(listaCLP,i)
        pre=nodo_capital.split("*")
        pais= pre[(len(pre)-1)]
        entry_pais= mp.get(mapa_paises, pais)
        if entry_pais== None:
            print(pais)
        minidic=me.getValue(entry_pais)
        loc_cap= ubicar_capital(minidic)
        lista=minidic['nodos_asoc']
        lta_vacia=lt.isEmpty(lista)
        if lta_vacia== False:
            j=0
            tamano2=lt.size(lista)
            while j<tamano2:
                nodo_pais=lt.getElement(lista,j)
                pre2= nodo_pais.split("-")
                lp= pre2[0]
                loc2= ubicarLp(lp, mapalp)
                dist=hs.haversine(loc_cap, loc2)
                addEdges(grafo,nodo_capital,nodo_pais, dist)
                j+=1
        else:
            lista_vertices= gr.vertices(grafo)
            nodocercano=findNearest(lista_vertices, loc_cap, mapalp)
            if nodocercano[1]!= None:
                addEdges(grafo,nodo_capital,nodocercano[0],nodocercano[1])
        i+=1

def ubicar_capital(minidic):
    info_pais=minidic['infopais']
    latitud=float(info_pais['CapitalLatitude'])
    longitud=float(info_pais['CapitalLongitude'])
    return (latitud, longitud)

def ubicarLp(lp,mapalp):
    latitud= None
    longitud= None
    entrylp=mp.get(mapalp,lp)
    if entrylp != None:
        diccionario=me.getValue(entrylp)
        info_lp = diccionario['lp']
        latitud=float(info_lp['latitude'])
        longitud= float(info_lp['longitude'])
    return (latitud,longitud)
    
def findNearest(lista_vertices, loc1, mapalp):
    menor=1000000000000.0000
    i=0
    tamano= lt.size(lista_vertices)
    retorno=None
    while i < tamano:
        dist=None
        elemento= lt.getElement(lista_vertices,i)
        pre= elemento.split('-')
        lp=pre[0]
        loc2=ubicarLp(lp,mapalp)
        if loc2!= (None,None):
            dist=hs.haversine(loc1, loc2)
            if dist< menor:
                menor= dist
                retorno=elemento
        i+=1
    return retorno, menor
    
# =================================
# Funciones para creacion de datos
# =================================

def formatVertex(cable,lp):    
    nombre_cable= cable['cable_id']
    nombre_nodo= lp + '-' + nombre_cable
    return nombre_nodo

# ======================
# Funciones de consulta
# ======================

# ================
# Requerimiento 1
# ================

def componentesConectados(analyzer):
    """ 
    Encuentra los componentes conectados usando el algoritmo de
    Kosaraju, lo guarda en el analyzer y mira el número de
    componentes conectados que tiene.

    Parámetros:
        analyzer: el catálogo donde está guardado todo.

    Retorna:
        un entero, que es el número de componentes conectados.
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    componentes = scc.connectedComponents(analyzer['components'])
    return componentes

def compareLpUserLpGraph(analyzer, landing_point1):
    """
    A partir de los landing points que ingresa el usuario, encuentra
    esos landing_point_id en los vértices y devuelve cada uno.

    Parámetros:
        analyzer: el catágologo donde está guardado todo.
        landing_point1: el landing point A ingresado por el usuario.

    
    Retorna:
        un string, que es el vértice correspondiente a landing_point1..
    """
    mapa = analyzer['connections']
    lista_llaves = gr.vertices(mapa)
    size = lt.size(lista_llaves)

    informacion = analyzer['info_lp']
    lista_lp = mp.keySet(informacion)
    tamaño_lp = lt.size(lista_lp)

    lpnumber = None

    i = 1
    centinelaA = False
    while i < tamaño_lp and centinelaA == False:
        elemento = lt.getElement(lista_lp, i)
        pareja = mp.get(informacion, elemento)
        valor = me.getValue(pareja)
        ciudad_pais = valor['lp']['name']
        cadena = ciudad_pais.split(',')
        nombre = cadena[0]
        if landing_point1 == nombre:
            #print('entré')
            lpnumber = elemento
            centinelaA = True
        i += 1

    j = 1
    centinelaB = False
    while j < size or centinelaB == False:
        cada_elemento = lt.getElement(lista_llaves, j)
        if cada_elemento[0] == '1' or cada_elemento[0] == '2' or cada_elemento[0] == '3' or cada_elemento[0] == '4' or cada_elemento[0] == '5' or cada_elemento[0] == '6' or cada_elemento[0] == '7' or cada_elemento[0] == '8' or cada_elemento[0] == '9' or cada_elemento[0] == '0':
            lp = cada_elemento.split('-')[0]
            if lp == lpnumber:
                centinelaB = True
                lpA = cada_elemento
        j += 1
     
    return lpA
        
def estanLosDosLandingPoints(analyzer, landing_point1, landing_point2):
    """
    Calcula si un landing point A está en el mismo clúster que
    un landing point B.

    Parámetros:
        analyzer: el catálogo donde está todo guardado.
        landing_point1: el landing point A ingresado por el usuario.
        landing_point2: el landing point B ingresado por el usuario.

    Retorna:
        un booleano, donde True significa que ambos landing points
        están en el mismo clúster. False significa que ambos landing
        points no están en el mismo clúster.
    """
    lpA = compareLpUserLpGraph(analyzer, landing_point1)
    lpB = compareLpUserLpGraph(analyzer, landing_point2)

    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    esta = scc.stronglyConnected(analyzer['components'], lpA, lpB)

    return esta

# ================
# Requerimiento 2
# ================

def lp_mas_cables(analyzer):
    mapa_lp = analyzer['info_lp']
    lista_landing_points = mp.keySet(mapa_lp)
    tamano_llp = lt.size(lista_landing_points)
    i = 0
    mayor = 0
    while i < tamano_llp:
        elemento = lt.getElement(lista_landing_points,i)
        entry = mp.get(mapa_lp, elemento)
        if entry != None:
            minidic = me.getValue(entry)
            mapa_cables = minidic['cables']
            lista_cables = mp.keySet(mapa_cables)
            cantidad_cables = lt.size(lista_cables)
            if cantidad_cables > mayor:
                mayor = cantidad_cables
                mas_cables = elemento
        i += 1

    lista_final = verificacion(mas_cables, analyzer, mayor)
    return (mayor, lista_final)

def verificacion(mas_cables, analyzer, mayor):
    mapa_lp = analyzer['info_lp']
    lista_landing_points = mp.keySet(mapa_lp)
    tamano_llp = lt.size(lista_landing_points)
    lp_ret = lt.newList('ARRAY_LIST')
    lt.addLast(lp_ret, mas_cables)
    i = 0
    while i < tamano_llp:
        elemento = lt.getElement(lista_landing_points,i)
        entry = mp.get(mapa_lp, elemento)
        if entry != None:
            minidic = me.getValue(entry)
            mapa_cables = minidic['cables']
            lista_cables = mp.keySet(mapa_cables)
            cantidad_cables = lt.size(lista_cables)
            if cantidad_cables == mayor:
                if elemento != mas_cables:
                    lt.addLast(lp_ret,elemento)
        i += 1

    return lp_ret

def infoLPmasCables(lp, analyzer):
    mapa_lp = analyzer['info_lp']
    entry = mp.get(mapa_lp,lp)
    minidic = me.getValue(entry)
    info_lp = minidic['lp']
    identificador = lp
    nombre = info_lp['name']
    pre = nombre.split(",")
    pais = pre[(len(pre) - 1)]
    return (nombre,pais,identificador)

# ================
# Requerimiento 3
# ================

def encontrarCapitalDePais(analyzer, pais):
    """
    Partiendo del pais, encuentra su capital.

    Parámetros:
        analyzer: el catálogo donde está guardado todo.
        pais: pais ingresado por el usuario.

    Retorna:
        un string, en el que queda el formato coorecto
        en el que está cada vértice, es decir,
        nombre_capital*nombre_pais.
    """
    formato = ''
    mapa_paises = analyzer['countries']
    pareja = mp.get(mapa_paises, pais)
    valor = me.getValue(pareja)
    infopais = valor['infopais']
    capital = infopais['CapitalName']
    formato = capital.lower() + '*' + pais
    return formato

def caminosMenorCosto(analyzer, pais):
    """
    Calcula los caminos de costo mínimo desde el pais ingresado
    por el usuario a todos los demás vértices del grafo.

    Parámetros:
        analyzer: el catálogo donde está guardado todo.
        pais: el pais de origen ingresado por el usuario.

    Retorna:
        el analyzer, donde en la llave 'paths' queda guardados
        los caminos de menor costo que devuleve el algortimo de
        Dijkstra.
    """
    paisini = encontrarCapitalDePais(analyzer, pais)
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], paisini)
    return analyzer

def caminoMenorCosto(analyzer, pais):
    """
    Calcula el camino de costo mínimo entre el pais origen
    (que se ingresa como parámetro en la función 'caminosMínimoCosto()')
    y el pais destino que se ingresa en esta función.
    Se debe ejecutar primero la función 'caminosMínimoCosto()'.

    Parámetros:
        analyzer: el catálogo donde está guardado todo.
        pais: el pais destino ingresado por el usuario.
    
    Retorna:
        el camino de costo mínimo entre el pais de origen
        y el pais destino.
    """
    paisfini = encontrarCapitalDePais(analyzer, pais)
    camino = djk.pathTo(analyzer['paths'], paisfini)
    return camino

def caminoMenorCostoLp(analyzer, landingA, landingB):
    lpA = compareLpUserLpGraph(analyzer, landingA)
    lpB = compareLpUserLpGraph(analyzer, landingB)

    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], lpA)
    camino = djk.pathTo(analyzer['paths'], lpB)
    return camino

# ================
# Requerimiento 4
# ================

# La idea es usar Prim para encontrar el árbol de expansión mínima. Con el árbol
# ya calculado, se necesita el size del keySet de la tabla de Hash que está
# en 'distTo' de la estructura 'search' que devuelve PrimMST() para encontrar el
# número de nodos que son parte del árbol. Para saber el costo total del árbol
# se puede usar weightMST(). 

# Ahora, para la conexión de mayor y menor distancia:
# Usar la funcion vertices para tener la lista de vértices del MST. Visitar cada vétice y usar
# Dijkstra (o DFS, está por verse) por cada vértice (con esto encontramos los caminos desde cada
# vértice hasta todos los vértices). De lo que devuelve eso se usa distTo para sacar la distancia
# entre el vértice A y todos los que tiene conexión. Ese valor se puede guardar en un diccionario
# estilo: {'conexion': vertexA-vertexB, 'costo': int} y cada uno de esos diccionarios se van guardando
# en una lista tipo array. Esa lista se puede ordenar de mayor a menor dependiendo del costo y con eso
# se tiene la conexión más larga y la más cortas.

# En realidad, todo el tema de Dijkstra se puede evitar si se usa la función 'scan' de Prim. Esta devuelve
# el costo total desde un vértice A hasta un vértice B. El resto (lo del diccionario y la lista) sí hay que
# hacerlo, pero lo de Dijkstra no es necesario.

def arbolExpansionMinima(analyzer):
    """
    Encuentra el árbol de expansión mínima.

    Parámetros:
        analyzer: el catálogo donde está guardado todo.

    Return:
        el árbol de expansión mínima. Este se guarda en el catálogo
        asociado a la llave 'mst'.
    """
    analyzer['mst'] = prim.PrimMST(analyzer['connections'])
    return analyzer['mst']

def totalVerticesMST(analyzer):
    """
    Devuelve el total de vértices del árbol de expansión mínima.

    Parámetros:
        analyzer: el catálogo donde está guardado todo.

    Return:
        un entero, que representa el total de vértices en el árbol.
    """
    mst = analyzer['mst']
    tabla = mst['distTo']
    lista = mp.keySet(tabla)
    total = lt.size(lista)
    return total

def costoTotalArcosMST(analyzer):
    """
    Devuelve el costo total del árbol de expansión mínima.

    Parámetros:
        analyzer: el catálogo donde está guardado todo.

    Return:
        un entero, que representa el costo total del árbol
        de expansión mínima.
    """
    grafo = analyzer['connections']
    mst = analyzer['mst']
    total = prim.weightMST(grafo, mst)
    return total

def distanciasMST(analyzer):
    """
    Crea dos diccionarios (uno para la distancia más larga
    y uno para la distancia más corta). Esto lo hace recorriendo
    los vértices y viendo la distancia desde uno origen hasta todos,
    comparando las distancias mayores y menores.

    Parámetros:
        analyzer: el catálogo donde está guardado todo.

    Retorna:
        una tupla, donde [0] es el diccionario de distancia y conexión
        mayor y [1] el diccionario de distancia y conexión menor.
    """
    grafo = analyzer['connections']
    mst = arbolExpansionMinima(analyzer)
    tabla = mst['distTo']
    lista = mp.keySet(tabla)
    tamaño = lt.size(lista)

    mayor = 0
    menor = 100000000000000000000000000000000

    dic_mayor = {}
    dic_menor = {}
    
    i = 1
    while i < tamaño:
        vertice = lt.getElement(lista, i)
        grafo_arbol = prim.prim(grafo, mst, vertice)

        j = 1
        while j < tamaño:
            cada_vertice = lt.getElement(lista, j)

            if cada_vertice != vertice:
                distancia_dic = prim.scan(grafo, grafo_arbol, cada_vertice)
                distancia_hash = distancia_dic['distTo']
                pareja = mp.get(distancia_hash, cada_vertice)
                distancia = me.getValue(pareja)
                
                if distancia > mayor:
                    mayor = distancia
                    dic_mayor['conexion'] = (vertice, cada_vertice)
                    dic_mayor['distancia'] = mayor
                elif distancia < menor:
                    menor = distancia
                    dic_menor['conexion'] = (vertice, cada_vertice)
                    dic_menor['distancia'] = menor

            j += 1
        i += 1

    return (dic_mayor, dic_menor)

# ================
# Requerimiento 5
# ================

def findLPfromName(nombre, catalog):
    mapa_nombres = catalog['nombres_lp']
    entry = mp.get(mapa_nombres,nombre)
    id_lp = me.getValue(entry)
    return id_lp

def findCountriesAffected(catalog, lp_id):
    mapa_lp = catalog['info_lp']
    entry = mp.get(mapa_lp, lp_id)
    minidic = me.getValue(entry)
    mapa_lps_asoc = minidic['LPsC']
    lista_lp_asoc = mp.keySet(mapa_lps_asoc)
    i = 1
    tamano = lt.size(lista_lp_asoc)
    lista_paises = lt.newList("ARRAY_LIST")
    while i < tamano+1:
        elemento = lt.getElement(lista_lp_asoc,i)
        entry = mp.get(mapa_lp, elemento)
        if entry != None:
            dic_list = {}
            entry2 = mp.get(mapa_lps_asoc, elemento)
            distancia = me.getValue(entry2)
            pais = findCountry(catalog,elemento)
            dic_list['pais'] = pais
            dic_list['distancia'] = distancia
            lt.addLast(lista_paises, dic_list)
        i += 1

    cantidad_paises = lt.size(lista_paises)
    lista_paises = SortbyDist(lista_paises)
    return (lista_paises, cantidad_paises)

# =========
# Limpieza
# =========

def limpieza(lista):
    """
    Convierte cualquier tipo de dato que es requerido temporalmente
    en None.
    """
    lista = None
    return lista

# ================================================================
# Funciones utilizadas para comparar elementos dentro de una lista
# =================================================================

def compareCountry(Id, entry):
    identry= me.getKey(entry)
    if Id == identry:
        return 0
    elif Id > identry:
        return 1
    else:
        return -1

def compareLPids(lp, lp2):
    lpid=lp2['key']
    if lp == lpid:
        return 0
    elif lp>lpid:
        return 1
    else:
        return-1

def comparePaises(pais1, pais2):
    if pais1 > pais2:
        return 1
    elif pais1 < pais2:
        return -1
    else:
        return 0

def comparedist(pais1,pais2):
    result = pais1['distancia'] > pais2['distancia']
    return result   
    
# =====================
# Funciones de formato
# =====================

def length(string):
    if string == "n.a.":
        string = 0
    else:    
        tamano = len(string)
        string = string[:(tamano-3)]
        string = string.replace(",","")
    return string
    
# ==========================
# Funciones de ordenamiento
# ==========================

def SortbyDist(lista):
    size = lt.size(lista)
    sub_list = lt.subList(lista, 0, size)
    sub_list = sub_list.copy()
    t1 = time.process_time()
    sorted_list = mer.sort(sub_list, comparedist)
    t2 = time.process_time()
    tiempo_ms = (t2-t1)*1000
    sub_list = None
    return (tiempo_ms, sorted_list) 