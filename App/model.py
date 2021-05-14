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


from DISClib.DataStructures.adjlist import addEdge
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
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
                    'info_LP': None,
                    'info_cables': None
                    }

        analyzer['countries'] = mp.newMap(numelements=220,
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
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model.newAnalyzer')

# Funciones para agregar informacion al catalogo
def addCountry(catalog, country):
    grafo=catalog['connections']
    paises= catalog['countries']
    name= country['\ufeffcountry_name'].lower()
    mp.put(paises,name, country)
    vert_cap= country['capital_name']
    if vert_cap=="N/A":
        vert_cap=country['\ufeffcountry_name'].lower()
    existscap= gr.containsVertex(grafo, vert_cap)
    if existscap==False:
        gr.insertVertex(grafo,vert_cap)

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
        if exists_destin== False:
            gr.insertVertex(grafo, destination)
        addEdge(grafo, origin, destination,weight)
        return catalog
        
    except Exception as exp:
        error.reraise(exp, 'model:addEdges')

def addEdges(grafo, origin, destination, weight):
    edge= gr.getEdge(grafo, origin, destination)
    if edge is None:
        gr.addEdge(grafo, origin, destination, weight)

def addcableInfo(link, catalog):
    nombre= link['cable_id']
    info_cables= catalog['info_cables']
    existe_cable=mp.contains(info_cables, nombre)
    if existe_cable==False:
        mp.put(info_cables,nombre,link)

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
