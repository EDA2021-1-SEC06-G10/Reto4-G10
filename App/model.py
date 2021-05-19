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
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
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

# Funciones para agregar informacion al catalogo
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


def addlp(catalog, info, nodo):
    lp_data= catalog['info_lp']
    mp.put(lp_data, nodo, info)

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
        InfoLp= me.getValue(entry)
        pre2=InfoLp['name'].split()
        pais_lp= pre2[(len(pre2)-1)]
    return pais_lp.lower()

def addLPtoCountry(pais, origin, catalog):
    paises=catalog['countries']
    entry=mp.get(paises, pais)
    if entry != None:
        minidic=me.getValue(entry)
        lista=minidic['nodos_asoc']
        lt.addLast(lista, origin)

def check(mapa, grafo):
    var=gr.containsVertex(grafo, "5808-colombian-festoon")
    value=mp.get(mapa,'colombia')
    print(var)
    return(value)    

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
        latitud=float(diccionario['latitude'])
        longitud= float(diccionario['longitude'])
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
    

# Funciones para creacion de datos
def formatVertex(cable,lp):    
    nombre_cable= cable['cable_id']
    nombre_nodo= lp + '-' + nombre_cable
    return nombre_nodo
# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
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

# Funcion de formato
def length(string):
    if string=="n.a.":
        string=0
    else:    
        tamano=len(string)
        string=string[:(tamano-3)]
        string= string.replace(",","")
    return string
    
# Funciones de ordenamiento
