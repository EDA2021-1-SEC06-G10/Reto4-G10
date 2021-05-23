﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 * MERCHANTABILITY or F ITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from math import pi
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Identificar los clústeres de comunicación")
    print("3- Identificar los puntos de conexión críticos de la red")
    print("4- Identificar la ruta de menor distancia")
    print("5- Identificar la Infraestructura crítica de la red")
    print("6- Análisis de fallas")
    print("0- Salir")

# ==========================================
# Sección de prints para cada requerimiento
# ==========================================

def print_Req1(landing_point1, landing_point2, booleano):
    print('*' * 25)
    if booleano == True:
        print('Por otro lado, ' + str(landing_point1) + ' y ' + str(landing_point2) + ' están en el mismo clúster.')
    else:
        print('Por otro lado, ' + str(landing_point1) + ' y ' + str(landing_point2) + ' no están en el mismo clúster.')
    print('*' * 25)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        analyzer=controller.initialize()
        controller.loadData(analyzer)
        vertices= gr.numVertices(analyzer['connections'])
        aristas= gr.numEdges(analyzer['connections'])
        #print(vertices, aristas)

    elif int(inputs[0]) == 2:
        # 5950 y 3210 están en el mismo clúster.
        # 5950 y 5774 no están en el mismo clúster.
        landing_point1 = '5950' #input('Ingrese el landing point A: ')
        landing_point2 = '3210' #input('Ingrese el landing point B: ')
        componentes = controller.componentesConectados(analyzer)
        estan = controller.estanLosDosLandingPoints(analyzer, landing_point1, landing_point2)
        print('*' * 25)
        print('El número de clústers es: ' + str(componentes))
        print_Req1(landing_point1, landing_point2, estan)

    elif int(inputs[0]) == 3:
        pais = 'albania'
        controller.encontrarCapitalDePais(analyzer, pais)
        #print(capital)

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    else:
        sys.exit(0)
sys.exit(0)
