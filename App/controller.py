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
 """

import config as cf
import model
import csv
from datetime import datetime
import time
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# ======================================
# Inicialización del Catálogo de cables
# ======================================

def initialize():
    analyzer=model.initialize()
    return analyzer

def loadData(catalog):
    loadlp(catalog)
    loadCountries(catalog)
    loadVertexescomp(catalog)
    loadnewEdges(catalog)
    connectCLP(catalog)

# =================================    
# Funciones para la carga de datos
# =================================

def loadnewEdges(catalog):
    grafo=catalog['connections']
    model.samelp(grafo)

def loadCountries(catalog):
    contentfile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for country in input_file:
        model.addCountry(catalog, country)

def loadVertexescomp(catalog):
    contentfile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for cable in input_file:
        cable['origin']=cable['\ufefforigin']
        cable['destination']= cable['destination']
        new_len=model.length(cable['cable_length'])
        cable["cable_length"]=float(new_len)
        model.addVertexescomp(catalog, cable)
    

def loadlp(catalog):
    contentfile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for lp in input_file:
        nodo = lp['landing_point_id']
        model.addlp(catalog, lp, nodo)

def connectCLP(catalog):
    model.connectCLP(catalog)

# ==========================
# Funciones de ordenamiento
# ==========================

# ========================================
# Funciones de consulta sobre el catalogo
# ========================================

def componentesConectados(analyzer):
    componentes = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()
   
    componentes =  model.componentesConectados(analyzer)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))

    return (componentes)

def compareLpUserLpGraph(analyzer, landing_point1):
    return model.compareLpUserLpGraph(analyzer, landing_point1)

def estanLosDosLandingPoints(analyzer, landing_point1, landing_point2):
    return model.estanLosDosLandingPoints(analyzer, landing_point1, landing_point2)

def encontrarCapitalDePais(analyzer, pais):
    return model.encontrarCapitalDePais(analyzer, pais)

def caminosMenorCosto(analyzer, pais):
    camino = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    camino = model.caminosMenorCosto(analyzer, pais)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))

    return (camino)

def caminoMenorCosto(analyzer, pais):
    lp = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()
   
    camino = model.caminoMenorCosto(analyzer, pais)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))

    return (camino)

def arbolExpansionMinima(analyzer):
    return model.arbolExpansionMinima(analyzer)

def conexionMasLargaMST(analyzer):
    return model.conexionMasLargaMST(analyzer)

def conexionMasCortaMST(analyzer):
    return model.conexionMasCortaMST(analyzer)

def caminoMenorCostoLp(analyzer, landingA, landingB):
    camino = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()
   
    camino = model.caminoMenorCostoLp(analyzer, landingA, landingB)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))
    return (camino)

def lp_mas_cables(analyzer):
    return model.lp_mas_cables(analyzer)

def infoLPmasCables(lp, analyzer):
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()
   
    lp = model.infoLPmasCables(lp, analyzer)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))

    return (lp)

def distanciasMST(analyzer):
    distancias = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()
   
    distancias = model.distanciasMST(analyzer)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))
    return (distancias)

def totalVerticesMST(analyzer):
    return model.totalVerticesMST(analyzer)

def costoTotalArcosMST(analyzer):
    return model.costoTotalArcosMST(analyzer)

def LpCualPais(analyzer, landing_point1, landing_point2):
    return model.LpCualPais(analyzer, landing_point1, landing_point2)

def paisDFS(analyzer, pais):
    return model.paisDFS(analyzer, pais)

def estaConectado(analyzer, pais):
    return model.estaConectado(analyzer, pais)

def totalPaisesAfectados(tabla):
    return model.totalPaisesAfectados(tabla)

def findLPfromName(nombre, catalog): 
    return model.findLPfromName(nombre, catalog)

def findCountriesAffected(catalog, lp_id):
    countries = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()
   
    countries = model.findCountriesAffected(catalog, lp_id)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))

    return (countries)

# ============================================
# Funciones para consulta de tiempo y memoria
# ============================================

def getTime():
    """
    Devuelve el instante de tiempo de procesamiento en milisegundos.
    """
    return float(time.perf_counter() * 1000)

def getMemory():
    """
    Toma una muestra de la memoria alocada en el instante de tiempo.
    """
    return tracemalloc.take_snapshot()

def deltaMemory(start_memory, stop_memory):
    """
    Calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

def limpieza(lista):
    """
    Llama a la función limpieza() del model.
    """
    return model.limpieza()