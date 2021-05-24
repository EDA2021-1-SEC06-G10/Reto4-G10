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


from math import dist
from DISClib.DataStructures.adjlist import addEdge
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
import DISClib.Algorithms.Graphs.dfs as dfs
import DISClib.Algorithms.Graphs.dijsktra as dij
import DISClib.Algorithms.Graphs.prim as prim
import DISClib.Algorithms.Graphs.scc as scc
import DISClib.Algorithms.Graphs.dfo as dfo
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
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
                    'info_lp': None,
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
    elLp=newLP(info)
    mp.put(lp_data, nodo, elLp)

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
        addConnectingLP(origin, destination, catalog)
        addConnectingLP(destination, origin, catalog)
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
        pre2=InfoLp['name'].split()
        pais_lp= pre2[(len(pre2)-1)]
    return pais_lp.lower()

def addConnectingLP(lp1, lp2, catalog):
    landing_points=catalog['info_lp']
    pre= lp1.split("-")
    lpO= pre[0]
    pre2= lp2.split('-')
    lpD=pre2[0]
    entry=mp.get(landing_points,lpO)
    if entry!= None:
        minidic= me.getValue(entry)
        InfoLp= minidic["LPsC"]
        mp.put(InfoLp, lpD, None)

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
            print(nodocercano[0],nodocercano[1])
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
        dist=-1
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

# La idea es pedirle al usuario que digite dos landing points. Luego,
# usar Kosaraju para encontrar/calcular los componentes conectados.
# Ahora, se puede usar sccCount() para saber cuántos componentes conectados
# hay. Esto es una parte. Para la otra, se tiene que usar stronglyConnected()
# para saber si los dos componentes ingresados están conectados (es decir, en
# el mismo clúster).

def componentesConectados(analyzer):
    """ 
    Encuentra los componentes conectados usando el algoritmo de
    Kosaraju, lo guarda en el analyzer y mira el número de
    componentes conectados que tiene.

    Parámetros:
        analyzer: el analyzer donde está guardado todo.

    Retorna:
        un entero, que es el número de componentes conectados.
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    componentes = scc.connectedComponents(analyzer['components'])
    return componentes

def compareLpUserLpGraph(analyzer, landing_point1, landing_point2):
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    mapa = analyzer['components']['idscc']

    lista_llaves = mp.keySet(mapa)
    size = lt.size(lista_llaves)

    i = 1
    centinelaA = False
    while i < size or centinelaA == False:
        cada_elemento = lt.getElement(lista_llaves, i)
        lp = cada_elemento.split('-')[0]
        if lp == landing_point1:
            centinelaA = True
            lpA = cada_elemento
        i += 1
    
    j = 1
    centinelaB = False
    while j < size or centinelaB == False:
        cada_elemento = lt.getElement(lista_llaves, j)
        lp = cada_elemento.split('-')[0]
        if lp == landing_point2:
            centinelaB = True
            lpB = cada_elemento
        j += 1
    
    return (lpA, lpB)
        
def estanLosDosLandingPoints(analyzer, landing_point1, landing_point2):
    """
    Calcula si un landing point A está en el mismo clúster que
    un landing point B.

    Parámetros:
        analyzer: es el analyzer donde está todo guardado.
        landing_point1: el landing point A ingresado por el usuario.
        landing_point2: el landing point B ingresado por el usuario.

    Retorna:
        un booleano, donde True significa que ambos landing points
        están en el mismo clúster. False significa que ambos landing
        points no están en el mismo clúster.
    """
    landing_points = compareLpUserLpGraph(analyzer, landing_point1, landing_point2)
    lpA = landing_points[0]
    lpB = landing_points[1]

    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    esta = scc.stronglyConnected(analyzer['components'], lpA, lpB)

    return esta

# ================
# Requerimiento 2
# ================

# ================
# Requerimiento 3
# ================

# La idea es pedirle al usuario 2 paises. Luego, se tiene que ver cuál es la
# capital de cada pais. Con las dos capitales se puede usar Dijkstra para
# encontrar el camino más corto entre los dos. Con el camino más corto, se
# usa distTo() para saber el costo desde el vértice capital1 hasta el vértice
# capital2. También, este requerimiento debería devolver el costo para cada
# par consecutivo de landing points. Toca pensarlo.

def encontrarCapitalDePais(analyzer, pais):
    mapa_paises = analyzer['countries']
    pareja = mp.get(mapa_paises, pais)
    valor = me.getValue(pareja)
    print(valor)


# ================
# Requerimiento 4
# ================

# La idea es usar Prim para encontrar el árbol de expansión mínima. Con el árbol
# ya calculado, se necesita usar numVertices() para encontrar el número de nodos
# que son parte del árbol. Para saber el costo total del árbol se puede usar
# weightMST(). La conexión más larga y la conexión más corta se podrían calcular
# usando la función edges() para tener una lista con todos los arcos. Esta lista
# se puede recorrer, viendo el peso de cada arco y viendo cual es menor y cual
# es mayor y así hasta sacar el mayor y el menor.

# ================
# Requerimiento 5
# ================

# La idea es que el usuario ingrese un landing point. Entonces, se tiene que ver
# ese landing point a qué pais pertenece y guardar ese pais. Se hace un DFS para
# saber a cuales otros landing points tiene camino el ingresado. Se puede usar
# ver vertices() para tener la lista de los vértices a los que puede llegar. Esta
# lista se recorre y se mira cada landing point a qué pais pertenece. Cada pais
# se va guardando en una Tabla de Hash (para asegurarnos que no hay paises repetidos).
# como la Tabla de Hash va a ser: {'llave': nombre_pais, 'valor': None} (eso no es literal
# una Tabla de Hash, es para que se entienda más fácil), hay que pedirle el el KeySet() y
# el size del KeySet(). Este size es el número de paises afectados. La lista de paises
# sería el KeySet() (o para mejor orden se puede recorrer ese KeySet y pasarlo a otra lista,
# pero no creo que valga la pena). Esta lista debería estar en orden de [km] decreciente, pero
# eso es un detalle para después.

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

# ===================
# Funcion de formato
# ===================

def length(string):
    if string=="n.a.":
        string=0
    else:    
        tamano=len(string)
        string=string[:(tamano-3)]
        string= string.replace(",","")
    return string
    
# Funciones de ordenamiento