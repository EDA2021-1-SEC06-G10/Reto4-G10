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
    return model.componentesConectados(analyzer)

def compareLpUserLpGraph(analyzer, landing_point1, landing_point2):
    return model.compareLpUserLpGraph(analyzer, landing_point1, landing_point2)

def estanLosDosLandingPoints(analyzer, landing_point1, landing_point2):
    return model.estanLosDosLandingPoints(analyzer, landing_point1, landing_point2)

def encontrarCapitalDePais(analyzer, pais):
    return model.encontrarCapitalDePais(analyzer, pais)

<<<<<<< HEAD
def caminosMenorCosto(analyzer, pais):
    return model.caminosMenorCosto(analyzer, pais)

def caminoMenorCosto(analyzer, pais):
    return model.caminoMenorCosto(analyzer, pais)

def arbolExpansionMinima(analyzer):
    return model.arbolExpansionMinima(analyzer)

def conexionMasLargaMST(analyzer):
    return model.conexionMasLargaMST(analyzer)

def conexionMasCortaMST(analyzer):
    return model.conexionMasCortaMST(analyzer)

def caminoMenorCostoLp(analyzer, landingA, landingB):
    return model.caminoMenorCostoLp(analyzer, landingA, landingB)

=======
def lp_mas_cables(analyzer):
    return model.lp_mas_cables(analyzer)

def infoLPmasCables(lp, analyzer):
    return model.infoLPmasCables(lp, analyzer)
>>>>>>> 7cfb6c55b633a03192291556b6e8fb612364cea5
# ============================================
# Funciones para consulta de tiempo y memoria
# ============================================