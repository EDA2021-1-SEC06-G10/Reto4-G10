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

# Inicialización del Catálogo de libros
def initialize():
    analyzer=model.initialize()
    return analyzer

def loadData(catalog):
    loadVertexescomp(catalog)
    loadCountries(catalog)
    #loadlp(catalog)
    
    

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
        cable["cable_length"]=int(float(new_len))
        model.addVertexescomp(catalog, cable)
    

def loadlp(catalog):
    contentfile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for lp in input_file:
        nodo = int(lp['\ufefflanding_point_id'])
        model.addlp(catalog, lp, nodo)

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catalogo
