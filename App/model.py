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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa

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
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }

        analyzer['countries'] = mp.newMap(numelements=220,
                                     maptype='PROBING',
                                     comparefunction=compareCountries)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=6000,
                                              comparefunction=compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
def addCountry(catalog, country):
    paises= catalog['countries']
    name= country['country_name']
    mp.put(paises,name, country)

def addVertexes(catalog, info, origin, destination):
    try:
        grafo= catalog['connections']
        existe_origin= gr.containsVertex(grafo, origin)
        existe_destino= gr.containsVertex(grafo, destination)
        if not existe_origin:
            gr.insertVertex(grafo, origin)
        if not existe_destino:
            gr.insertVertex(grafo, destination)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addVertexes')


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compareCountries(country, countryname):
    Cntry= countryname['country_name']
    if country== Cntry:
        return 0
    elif country>Cntry:
        return 1
    else:
        return -1

# Funciones de ordenamiento
