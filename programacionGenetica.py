#Algoritmo que resuelve problemas por tecnica de programacion genetica
#CarlosAEH1

import math
import random
from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

def codificarCromosoma(cromosoma, limite, numeros):
	bits=len(numeros[0])
	bit=0
	pesos=0
	numero=[]
	peso=[]
	while(bit<len(cromosoma)):				#Recorre cada bit
		numero+=[cromosoma[bit]]
		bit+=1
		if(len(numero)==bits):				#Divide cromosoma en grupos de 4 bits consecutivos
			pesos+=1
			for k in range(limite):			#Compara grupo de 4 bits con los numeros binarios
				if(numero==numeros[k]):
					peso+=[k]
					break
			if(pesos!=len(peso)): peso+=[0]		#Ignora numeros binarios no reconocidos
			numero=[]
	#print('-Peso: '+str(peso))
	return peso

def codificarCromosomas(cromosomas, limite, numeros):
	pesos=[]
	for i in range(len(cromosomas)):
		cromosoma=cromosomas[i]
		peso=codificarCromosoma(cromosoma, limite,  numeros)
		pesos+=[peso]
	#print('\nPesos de cromosomas: ')
	#for i in range(len(pesos)): print('-Cromosoma ', i+1, ': ', pesos[i])
	return pesos

def evaluarArbolBooleano(nodos, entrada, nivel, profundidad):
	#print('Nodos: ', nodos)
	#print('Nivel: ', nivel)
	#print('Profundidad: ', profundidad)
	if(nivel<profundidad):									#Opera nodo
		if(nodos[0]==0):								#Verifica primer operador de árbol (and)
			del nodos[0]								#Elimina primer operador de árbol
			operando1=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)	#Evalua resto de árbol para obtener primer operando, aumentando el nivel de profundidad.
			operando2=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)	#Evalua resto de árbol para obtener segundo operando, aumentando el nivel de profundidad.
			salida=(operando1 and operando2)					#Opera and
			nivel-=1								#Retorno de nivel
		elif(nodos[0]==1):								#Verifica primer operador de árbol (or)
			del nodos[0]
			operando1=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			operando2=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			salida=(operando1 or operando2)
			nivel-=1
		elif(nodos[0]==2):								#Verifica primer operador de árbol (not)
			del nodos[0]								#Elimina primer operador de árbol
			operando=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)	#Evalua resto de árbol para obtener operando, aumentando el nivel de profundidad.
			salida=not(operando)							#Opera not
			nivel-=1								#Retorno de nivel
		elif(nodos[0]==3):								#Verifica primer operador de árbol (xor)
			del nodos[0]
			operando1=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			operando2=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			salida=(operando1 and not(operando2))or(not(operando1) and operando2)
			nivel-=1
	else:
		del nodos[0]									#Elimina primer nodo de arbol
		salida=bool(entrada[0])								#Asigna variable a terminal
		#print('Entrada: ', salida)
		del entrada[0]									#Elimina primer variable de entrada
	return salida

def evaluarArbolAlgebraico(nodos, k, x, nivel, profundidad):					#Recorre cromosoma como arbol en preorden
	#print('Nodos: ', nodos)
	#print('Nivel: ', nivel)
	#print('Profundidad: ', profundidad)
	if(nivel<profundidad):									#Verifica nivel de profundidad
		if(nodos[0]==0):								#Verifica primer operador de árbol
			del nodos[0]								#Elimina primer operador de árbol
			operando1=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)	#Evalua resto de árbol para obtener primer operando, aumentando de nivel.
			operando2=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)	#Evalua resto de árbol para obtener segundo operando, aumentando de nivel.
			resultado=operando1+operando2						#Opera suma
			nivel-=1								#Retorno de nivel
		elif(nodos[0]==1):								#Verifica primer operador de árbol
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			resultado=-operando
			nivel-=1
		elif(nodos[0]==2):								#Verifica primer operador de árbol
			del nodos[0]
			operando1=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			operando2=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			resultado=operando1-operando2
			nivel-=1
		elif(nodos[0]==3):								#Verifica primer operador de árbol
			del nodos[0]
			operando1=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			operando2=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			resultado=operando1*operando2
			nivel-=1
		elif(nodos[0]==4):								#Verifica primer operador de árbol
			del nodos[0]
			operando1=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			operando2=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			if(operando2==0): resultado=operando1
			else: resultado=operando1/operando2
			nivel-=1
		elif(nodos[0]==5):								#Verifica primer operador de árbol
			del nodos[0]								#Elimina primer operador de árbol
			operando=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)	#Evalua resto de árbol para obtener operador, aumentando de nivel.
			resultado=math.sin(operando)						#Opera seno
			nivel-=1								#Retorno de nivel
		elif(nodos[0]==6):								#Verifica primer operador de árbol
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			resultado=math.cos(operando)
			nivel-=1
		elif(nodos[0]==7):								#Verifica primer operador de árbol
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			resultado=math.tan(operando)
			nivel-=1
		elif(nodos[0]==8):								#Verifica primer operador de árbol
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			resultado=math.sqrt(abs(operando))
			nivel-=1
		elif(nodos[0]==9):								#Verifica primer operador de árbol
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, k, x, nivel+1, profundidad)
			if(operando==0): resultado=operando
			else: resultado=math.log(abs(operando))
			nivel-=1
	else:
		if(nodos[0]%2==0): resultado=k							#Si primer nodo de arbol es par, se asigna constante a terminal.
		else: resultado=x								#Si primer nodo de arbol es impar, se asigna variable a terminal.
		del nodos[0]									#Elimina primer nodo de arbol
		#print('Entrada: ', resultado)
	return resultado

def evaluarParidad(cromosomas, profundidad, numeros, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior):
	entradasFuncion=[[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]
	salidasFuncion=[1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
	#print('\n\nEvaluación')
	pesos=codificarCromosomas(cromosomas, 4, numeros)
	resultados=[]
	errores=[]
	utilidades=[]
	for i in range(len(pesos)):																												#Recorre cada modelo de la poblacion
		pesosCromosoma=pesos[i]																												#Modelo a evaluar
		resultadosCromosoma=[]
		erroresCromosoma=[]
		for j in range(len(entradasFuncion)):																										#Recorre conunto de entrada
			nodos=pesosCromosoma[:]																											#Copia modelo
			numero=entradasFuncion[j]																										#Entrada
			entrada=numero[:]																											#Copia entrada
			entrada+=entrada																											#Duplica entrada
			salida=evaluarArbolBooleano(nodos, entrada, 0, profundidad)																						#Evalua modelo
			#print('Resultado de cromosoma: '+str(salida))
			resultadosCromosoma+=[int(salida)]																									#Resultados de modelo
			erroresCromosoma+=[abs(salidasFuncion[j]-int(salida))]																							#Calcula error absoluto
			#print('Errores de cromosoma: '+str(erroresCromosoma))
		resultados+=[resultadosCromosoma]																										#Resultados de modelos
		errores+=[erroresCromosoma]																											#Errores de modelos
		utilidades+=[sum(erroresCromosoma)]																										#Utilidad de modelos
	#print('\nResultados de cromosomas: ')
	#for i in range(len(resultados)): print('-Cromosoma ', i+1, ': ', resultados[i])
	#print('\nErrores de cromosomas: ')
	#for i in range(len(errores)): print('-Cromosoma ', i+1, ': ', errores[i])
	#print('\nError de cromosomas: ')
	#for i in range(len(utilidades)): print('-Cromosoma ', i+1, ': ', utilidades[i])
	cromosomaElitista, utilidadElitistaActual=mejorar(cromosomas, utilidades, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior)															#Implementa elitismo
	aptitud=sum(utilidades)
	#print('\nUtilidad de la poblacion: ', aptitud)
	aptitudes=[]
	if(aptitud!=0):
		for i in range(len(utilidades)): aptitudes+=[utilidades[i]/aptitud]
	else: aptitudes=utilidades
	return aptitudes, cromosomaElitista, utilidadElitistaActual, aptitud

def evaluarRegresionCoordenadas(cromosomas, coordenadas, inferiorX, superiorX, profundidad, numeros, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior, constante):
	#print('\n\nEvaluación de coordenadas')
	pesos=codificarCromosomas(cromosomas, 10, numeros)
	if(constante==None): constante=random.randrange(10)																	#Genera constante aleatoria
	else:																					#Actualiza constante
		if(constante!=0): constante=ceil((constante+random.randrange(constante))/2)
	#print('\nConstante: ', constante)
	resultados=[]
	errores=[]
	utilidades=[]
	for i in range(len(pesos)):																		#Recorre cada modelo de la población
		pesosCromosoma=pesos[i]																		#Modelo a evaluar
		resultadosCromosoma=[]
		erroresCromosoma=[]
		for j in range(len(coordenadas)):																#Recorre coordenadas
			coordenada=coordenadas[j]																#Coordenada (x, y)
			#print('-('+str(coordenada[0])+', '+str(coordenada[1])+')')
			nodos=pesosCromosoma[:]																	#Copia modelo
			resultadoCromosoma=evaluarArbolAlgebraico(nodos, constante, float(coordenada[0]), 0, profundidad)							#Evalua modelo
			#print('-Resultado de cromosoma: '+str(resultadoCromosoma))
			resultadosCromosoma+=[resultadoCromosoma]
			erroresCromosoma+=[abs(float(coordenada[1])-resultadoCromosoma)]											#Calcula error absoluto
			#print('Errores de cromosoma: '+str(erroresCromosoma))
		if float('inf') in erroresCromosoma:																#Evita valores infinitos
			posicion=erroresCromosoma.index(float('inf'))
			del erroresCromosoma[posicion]
		resultados+=[resultadosCromosoma]																#Resultados de modelos
		errores+=[erroresCromosoma]																	#Errores de modelos
		utilidades+=[sum(erroresCromosoma)]																#Utilidades de modelos
	#print('\nResultados de cromosomas: ')
	#for i in range(len(resultados)): print('-Cromosoma ', i+1, ': ', resultados[i])
	#print('\nErrores de cromosomas: ')
	#for i in range(len(errores)): print('-Cromosoma ', i+1, ': ', errores[i])
	#print('\nError de cromosomas: ')
	#for i in range(len(utilidades)): print('-Cromosoma ', i+1, ': ', utilidades[i])
	cromosomaElitista, utilidadElitistaActual=mejorar(cromosomas, utilidades, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior)					#Implementa elitismo
	aptitud=sum(utilidades)
	#print('\nUtilidad de la poblacion: ', aptitud)
	aptitudes=[]
	if(aptitud!=0):
		for i in range(len(utilidades)): aptitudes+=[utilidades[i]/aptitud]
	else: aptitud=utilidades
	return aptitudes, cromosomaElitista, utilidadElitistaActual, aptitud, constante

def evaluarRegresionExpresion(cromosomas, inferiorX, superiorX, profundidad, numeros, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior, constante):
	#print('\n\nEvaluación de expresion')
	pesos=codificarCromosomas(cromosomas, 10, numeros)
	if(constante==None): constante=random.randrange(10)													#Genera constante aleatoria
	else:																			#Actualiza constante
		if(constante!=0): constante=ceil((constante+random.randrange(constante))/2)
	#print('\nConstante: ', k)
	resultados=[]
	errores=[]
	utilidades=[]
	for i in range(len(pesos)):																#Recorre cada modelo de la población
		pesosCromosoma=pesos[i]																#Modelo a evaluar
		resultadosCromosoma=[]
		erroresCromosoma=[]
		x=inferiorX																	#Limite inferior de variable independiente
		while(x<=superiorX):																#Recorre rango de variable independiente															#Recorre rango de variable independiente
			resultadoFuncion=((-2.34**3)-(-0.11*x/2))+23.45												#Evalua funcion
			#print('\n-Resultado de funcion: '+str(resultadoFuncion))
			nodos=pesosCromosoma[:]															#Copia modelo
			resultadoCromosoma=evaluarArbolAlgebraico(nodos, constante, x, 0, profundidad)								#Evalua modelo
			#print('-Resultado de cromosoma: '+str(resultadoCromosoma))
			resultadosCromosoma+=[resultadoCromosoma]
			erroresCromosoma+=[abs(resultadoFuncion-resultadoCromosoma)]										#Calcula error absoluto
			#print('Errores de cromosoma: '+str(erroresCromosoma))
			x=round(x+0.1, 1)															#Incrementa variable independiente
		resultados+=[resultadosCromosoma]														#Resultados de modelos
		errores+=[erroresCromosoma]															#Errores de modelos
		utilidades+=[sum(erroresCromosoma)]														#Utilidades de modelos
	#print('\nResultados de cromosomas: ')
	#for i in range(len(resultados)): print('-Cromosoma ', i+1, ': ', resultados[i])
	#print('\nErrores de cromosomas: ')
	#for i in range(len(errores)): print('-Cromosoma ', i+1, ': ', errores[i])
	#print('\nError de cromosomas: ')
	#for i in range(len(utilidades)): print('-Cromosoma ', i+1, ': ', utilidades[i])
	cromosomaElitista, utilidadElitistaActual=mejorar(cromosomas, utilidades, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior)			#Implementa elitismo
	aptitud=sum(utilidades)
	#print('\nUtilidad de la poblacion: ', aptitud)
	aptitudes=[]
	if(aptitud!=0):
		for i in range(len(utilidades)): aptitudes+=[utilidades[i]/aptitud]
	else: aptitud=utilidades
	return aptitudes, cromosomaElitista, utilidadElitistaActual, aptitud, constante

def leerCoordenadas(nombre):
	contenido=open(nombre+'.txt')
	coordenadas=[]
	for linea in contenido: coordenadas+=[linea.rstrip().split('\t')]	#Obtiene coordendas de archivo TXT
	#print('\nCoordenadas')
	#for i in range(len(coordenadas)): print(str(coordenadas[i]))
	coordenada=coordenadas[0]						#Coordenada (x, y)
	inferiorX=coordenada[0]
	coordenada=coordenadas[len(coordenadas)-1]				#Limite inferior de x
	superiorX=coordenada[0]							#Limite superior de x
	return coordenadas, inferiorX, superiorX

numeros4=[[0, 0], [0, 1], [1, 0], [1, 1]]
numeros8=[[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
numeros16=[[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]	#Numeros binarios

#coordenadas, inferiorX, superiorX=leerCoordenadas(nombre)
cromosomas=generarPoblacion(tamanoCromosoma, tamanoPoblacion)
aptitudes, cromosomaElitista, utilidadElitista, aptitud, constante=evaluarRegresionExpresion(cromosomas, inferiorX, superiorX, profundidad, numeros16, opcionSeleccion, None, None, None)
#aptitudes, cromosomaElitista, utilidadElitista, aptitud, constante=evaluarRegresionCoordenadas(cromosomas, coordenadas, inferiorX, superiorX, profundidad, numeros16, opcionSeleccion, None, None, None)
#aptitudes, cromosomaElitista, utilidadElitista, aptitud=evaluarParidad(cromosomas, profundidad, numeros4, opcionSeleccion, None, None)
for j in range(generaciones):
	cromosomas=seleccionar(cromosomas, aptitudes, opcionSeleccion)
	cromosomas=cruzar(cromosomas, probabilidadCruza)
	cromosomas=mutar(cromosomas, probabilidadMutacion)
	aptitudes, cromosomaElitista, utilidadElitista, aptitud, constante=evaluarRegresionExpresion(cromosomas, inferiorX, superiorX, profundidad, numeros16, opcionSeleccion, cromosomaElitista, utilidadElitista, constante)
	#aptitudes, cromosomaElitista, utilidadElitista, aptitud, constante=evaluarRegresionCoordenadas(cromosomas, coordenadas, inferiorX, superiorX, profundidad, numeros16, opcionSeleccion, cromosomaElitista, utilidadElitista, constante)
	#aptitudes, cromosomaElitista, utilidadElitista, aptitud=evaluarParidad(cromosomas, profundidad, numeros4, opcionSeleccion, cromosomaElitista, utilidadElitista)
