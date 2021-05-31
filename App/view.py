"""
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
from typing import runtime_checkable
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr
from DISClib.ADT import stack as stk
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
    print("4- Establecer estación base")
    print("5- Identificar la ruta de menor distancia")
    print("6- Identificar la Infraestructura crítica de la red")
    print("7- Análisis de fallas")
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

def print_Req3(camino):
    if camino is not None:
        distCamino = stk.size(camino)
        print('El camino es de longitud: ' + str(distCamino) + '.')
        while (not stk.isEmpty(camino)):
            cada_vertice = stk.pop(camino)
            print(cada_vertice)
    else:
        print('No hay camino.')

def printResultsReq2(info_lp, cantidad_cables):
    print('*' * 25)
    print('El landing point: '+ info_lp[0] + " con numero de identificacion: " +info_lp[2]+ " se encuentra en" +info_lp[1])
    print("Este tiene un total de " + str(cantidad_cables)+ " cables conectados a el")

def printReq5(resultado, lp_name):
    print('*' * 25)
    print('Si falla el landing point: '+ lp_name + " habría  " +str(resultado[1])+ " paises afectados")
    print('\nEstos paises son: ')
    i=0
    tamano=lt.size(resultado[0][1])
    while i < tamano:
        dic= lt.getElement(resultado[0][1], i)
        pais=dic['pais']
        distancia=dic['distancia']
        print(pais+ " se encontraría afectado y tiene un lp a " +str(distancia)+ " km")
        i+=1

    

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
        # 5950 (Port Sudan) y 3210 (Marseille) están en el mismo clúster.
        # 5950 y 5774 no están en el mismo clúster.
        landing_point1 = '5950' #input('Ingrese el landing point A: ')
        landing_point2 = '3210' #input('Ingrese el landing point B: ')
        componentes = controller.componentesConectados(analyzer)
        estan = controller.estanLosDosLandingPoints(analyzer, landing_point1, landing_point2)
        print('*' * 25)
        print('El número de clústers es: ' + str(componentes))
        print_Req1(landing_point1, landing_point2, estan)

    elif int(inputs[0]) == 3:
        resultado=controller.lp_mas_cables(analyzer)
        i=0 
        tamano= lt.size(resultado[1])
        while i < tamano:
            lp=lt.getElement(resultado[1],i)
            info_del_lp= controller.infoLPmasCables(lp,analyzer)
            printResultsReq2(info_del_lp, resultado[0])
            i+=1

    elif int(inputs[0]) == 4:
        pais_ini = 'uruguay' #input('Ingrese el pais de origen: ')
        formato = controller.encontrarCapitalDePais(analyzer, pais_ini)
        controller.caminosMenorCosto(analyzer, formato)
        print(formato)

    elif int(inputs[0]) == 5:
        landingA = '5950'
        landingB = '5825'
        pais_fini = 'argentina' #input('Ingrese el pais destino: ')
        #formato = controller.encontrarCapitalDePais(analyzer, pais_fini)
        camino = controller.caminoMenorCostoLp(analyzer, landingA, landingB)
        #camino = controller.caminoMenorCosto(analyzer, formato)
        #print(formato)
        print_Req3(camino)

    elif int(inputs[0]) == 6:
<<<<<<< HEAD
        #mst  = controller.arbolExpansionMinima(analyzer)
        distancias = controller.distanciasMST(analyzer)
        #total = controller.totalVerticesMST(analyzer)
        #costo = controller.costoTotalArcosMST(analyzer)
        print(distancias)
=======
        nombrelp=input("Ingrese el nombre del landing point: ")
        nombrelp=nombrelp.lower()
        id_lp=controller.findLPfromName(nombrelp, analyzer)
        print(id_lp)
        resultado= controller.findCountriesAffected(analyzer,id_lp)
        print(resultado[0])
        printReq5(resultado, nombrelp)
        
>>>>>>> c12e548469c5390f131ff30fc06c3de4e053a71b

    elif int(inputs[0]) == 7:
        landing_point1 = '5950'
        landing_point2 = '5825'
        formato = controller.LpCualPais(analyzer, landing_point1, landing_point2)
        controller.paisDFS(analyzer, formato)
        tabla = controller.estaConectado(analyzer, formato)
        total = controller.totalPaisesAfectados(tabla)
        print(total[0])
        print(total[1])

    else:
        sys.exit(0)
sys.exit(0)
