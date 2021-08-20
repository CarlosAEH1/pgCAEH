#Algoritmo que resuelve problemas por tecnica de programacion genetica
#CarlosAEH1

def mostrarCromosomas(cromosomas):
	print('\n\nPoblacion\n')
	for i in range(len(cromosomas)): print('Cromosoma ', i+1, ': '+str(cromosomas[i]))

def mutar(cromosomas, probabilidad):
	#print('\n\nMutacion')
	for i in range(len(cromosomas)):
		#print('\nCromosoma ', i+1)
		cromosoma=cromosomas[i]
		for j in range(len(cromosoma)):
			aleatorio=random.random()
			if(aleatorio<=probabilidad):
				#print('-Posicion ', j, ', con numero aleatorio: ', aleatorio)
				if(cromosoma[j]==0): cromosoma[j]=1
				else: cromosoma[j]=0
		cromosomas[i]=cromosoma
	#mostrarCromosomas(cromosomas)
	return cromosomas

def cruzar(cromosomas, probabilidad):
	#print('\n\nCruza\n')
	indicesCruza=[]
	for i in range(len(cromosomas)):
		aleatorio=random.random()
		if(aleatorio<=probabilidad):							#Seleeciona cromosomas a cruzarse
			#print('Cromosoma ', i+1, ', con numero aleatorio: ', aleatorio)
			indicesCruza+=[i]
	if(len(indicesCruza)%2==1): del indicesCruza[-1]					#Verifica cantidad par de crozomas a cruzarse
	pareja=[]
	cromosomasCruzados=[]
	for i in range(len(cromosomas)):
		for j in range(len(indicesCruza)):
			if(i==indicesCruza[j]): pareja+=[cromosomas[i]]				#Busca cromosoma a cruzarse
		if(len(pareja)==2):								#Cruza cromosomas
			padre1=pareja[0]
			padre2=pareja[1]
			pareja=[]
			#print('\nPadre 1: ', padre1)
			#print('Padre 2: ', padre2)
			posicion=random.randrange(len(cromosomas[i]))
			#print('\nPosicion de cruza: ', posicion)
			hijo1=[]
			hijo2=[]
			for k in range(len(cromosomas[i])):
				if(k<posicion):
					hijo1+=[padre1[k]]
					hijo2+=[padre2[k]]
				else:
					hijo1+=[padre2[k]]
					hijo2+=[padre1[k]]
			#print('\nHijo 1: ', hijo1)
			#print('Hijo 2: ', hijo2)
			cromosomasCruzados+=[hijo1]+[hijo2]
	for i in range(len(cromosomas)):							#Sustituye cromosomas originales
		for j in range(len(indicesCruza)):
			if(i==indicesCruza[j]): cromosomas[i]=cromosomasCruzados[j]
	#mostrarCromosomas(cromosomas)
	return cromosomas

def seleccionar(cromosomas, aptitudesRelativas, opcionSeleccion):
	#print('\n\nSelecion\n')
	aptitudAcumulada=0
	aptitudesAcumuladas=[]
	#print('Cromosoma\tAptitud relativa\tAptitud acumulada')
	for i in range(len(aptitudesRelativas)):							#Calcula aptitud acumulada
		aptitudAcumulada+=aptitudesRelativas[i]
		#print(str(i+1)+'\t'+str(aptitudesRelativas[i])+'\t'+str(aptitudAcumulada))
		aptitudesAcumuladas+=[aptitudAcumulada]
	cromosomasSeleccionados=[]
	#print('\n')
	for i in range(len(cromosomas)):								#Selecciona cromosomas
		aleatorio=random.random()
		for j in range(len(aptitudesAcumuladas)):
			if(aptitudesAcumuladas[j]>aleatorio):
				if(opcionSeleccion==1): cromosomasSeleccionados+=[cromosomas[j]]	#Maximizacion de aptitud acumulada
				elif(opcionSeleccion==2): cromosomasSeleccionados+=[cromosomas[j-1]]	#Minimizacion de aptitud acumulada
				break
	#mostrarCromosomas(cromosomasSeleccionados)
	return cromosomasSeleccionados

def mejorar(cromosomas, utilidades, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior):
	if(opcionSeleccion==1):										#Obtiene el mejor cromosoma
		utilidadElitistaActual=max(utilidades)
		if(utilidadElitistaAnterior is None): utilidadElitistaAnterior=utilidadElitistaActual
		if(utilidadElitistaAnterior>utilidadElitistaActual):					#Sustituye peor cromosoma por mejor cromosoma
			utilidadVulgar=min(utilidades)
			posicion=utilidades.index(utilidadVulgar)
			cromosomas[posicion]=cromosomaElitista
			utilidades[posicion]=utilidadElitistaAnterior
			utilidadElitistaActual=utilidadElitistaAnterior
		else:
			posicion=utilidades.index(utilidadElitistaActual)
			cromosomaElitista=cromosomas[posicion]
	elif(opcionSeleccion==2):									#Obtiene el mejor cromosoma
		utilidadElitistaActual=min(utilidades)
		if(utilidadElitistaAnterior is None): utilidadElitistaAnterior=utilidadElitistaActual
		if(utilidadElitistaAnterior<utilidadElitistaActual):					#Sustituye peor cromosoma por mejor cromosoma
			utilidadVulgar=max(utilidades)
			posicion=utilidades.index(utilidadVulgar)
			cromosomas[posicion]=cromosomaElitista
			utilidades[posicion]=utilidadElitistaAnterior
			utilidadElitistaActual=utilidadElitistaAnterior
		else:
			posicion=utilidades.index(utilidadElitistaActual)
			cromosomaElitista=cromosomas[posicion]
	return cromosomaElitista, utilidadElitistaActual

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

def evaluarArbolBooleano(nodos, entrada, nivel, profundidad):					#Recorre cromosoma como arbol en preorden
	#print('Nodos: ', nodos)
	#print('Nivel: ', nivel)
	#print('Profundidad: ', profundidad)
	if(nivel<profundidad):									#Opera nodo
		if(nodos[0]==0):
			del nodos[0]
			operando1=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			operando2=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			salida=(operando1 and operando2)
			nivel-=1
		elif(nodos[0]==1):
			del nodos[0]
			operando1=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			operando2=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			salida=(operando1 or operando2)
			nivel-=1
		elif(nodos[0]==2):
			del nodos[0]
			operando=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			salida=not(operando)
			nivel-=1
		elif(nodos[0]==3):
			del nodos[0]
			operando1=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			operando2=evaluarArbolBooleano(nodos, entrada, nivel+1, profundidad)
			salida=(operando1 and not(operando2))or(not(operando1) and operando2)
			nivel-=1
	else:
		del nodos[0]									#Agrega nodo varable o contante aleatoriamente
		salida=bool(entrada[0])
		#print('Entrada: ', salida)
		del entrada[0]
	return salida

def evaluarArbolAlgebraico(nodos, entrada, nivel, profundidad):					#Recorre cromosoma como arbol en preorden
	#print('Nodos: ', nodos)
	#print('Nivel: ', nivel)
	#print('Profundidad: ', profundidad)
	if(nivel<profundidad):									#Opera nodo
		if(nodos[0]==0):
			del nodos[0]
			operando1=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			operando2=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			resultado=operando1+operando2
			nivel-=1
		elif(nodos[0]==1):
			del nodos[0]
			operando1=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			operando2=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			resultado=operando1-operando2
			nivel-=1
		elif(nodos[0]==2):
			del nodos[0]
			operando1=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			operando2=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			resultado=operando1*operando2
			nivel-=1
		elif(nodos[0]==3):
			del nodos[0]
			operando1=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			operando2=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			if(operando2==0): resultado=operando1
			else: resultado=operando1/operando2
			nivel-=1
		elif(nodos[0]==4):
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			resultado=math.sin(operando)
			nivel-=1
		elif(nodos[0]==5):
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			resultado=math.cos(operando)
			nivel-=1
		elif(nodos[0]==6):
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			resultado=math.tan(operando)
			nivel-=1
		elif(nodos[0]==7):
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			if(operando<0): resultado=operando
			else: resultado=math.sqrt(operando)
			nivel-=1
		elif(nodos[0]==8):
			del nodos[0]
			operando=evaluarArbolAlgebraico(nodos, entrada, nivel+1, profundidad)
			if(operando<=0): resultado=operando
			else: resultado=math.log(operando)
			nivel-=1
	else:
		del nodos[0]									#Agrega nodo varable o contante aleatoriamente
		resultado=entrada[0]
		#print('Entrada: ', resultado)
		del entrada[0]
	return resultado

def evaluarParidad(cromosomas, profundidad, numeros, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior):
	entradasFuncion=[[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]
	salidasFuncion=[1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
	#print('\n\nEvaluación')
	pesos=codificarCromosomas(cromosomas, 4, numeros)
	resultados=[]
	errores=[]
	utilidades=[]
	for i in range(len(pesos)):
		pesosCromosoma=pesos[i]
		resultadosCromosoma=[]
		erroresCromosoma=[]
		for j in range(len(entradasFuncion)):
			nodos=pesosCromosoma[:]
			numero=entradasFuncion[j]
			entrada=numero[:]
			salida=evaluarArbolBooleano(nodos, entrada, 0, profundidad)																					#Evalua cromosoma
			#print('Resultado de cromosoma: '+str(salida))
			resultadosCromosoma+=[int(salida)]
			erroresCromosoma+=[abs(salidasFuncion[j]-int(salida))]																						#Calcula error absoluto
			#print('Errores de cromosoma: '+str(erroresCromosoma))
		resultados+=[resultadosCromosoma]
		errores+=[erroresCromosoma]																										#Calcula utilidad de cromosoma
		utilidades+=[sum(erroresCromosoma)]
	#print('\nResultados de cromosomas: ')
	#for i in range(len(resultados)): print('-Cromosoma ', i+1, ': ', resultados[i])
	#print('\nErrores de cromosomas: ')
	#for i in range(len(errores)): print('-Cromosoma ', i+1, ': ', errores[i])
	#print('\nError de cromosomas: ')
	#for i in range(len(utilidades)): print('-Cromosoma ', i+1, ': ', utilidades[i])
	cromosomaElitista, utilidadElitistaActual=mejorar(cromosomas, utilidades, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior)	#Implementa elitismo
	aptitud=sum(utilidades)
	#print('\nUtilidad de la poblacion: ', aptitud)
	aptitudes=[]
	for i in range(len(utilidades)): aptitudes+=[utilidades[i]/aptitud]
	return aptitudes, cromosomaElitista, utilidadElitistaActual, aptitud

def evaluarRegresion(cromosomas, inferiorX, superiorX, profundidad, nombre, numeros, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior):
	#print('\n\nEvaluación')
	pesos=codificarCromosomas(cromosomas, 9, numeros)
	resultados=[]
	errores=[]
	utilidades=[]
	for i in range(len(pesos)):
		pesosCromosoma=pesos[i]
		resultadosCromosoma=[]
		erroresCromosoma=[]
		k=random.random()
		#print('\nAleatorio de cromosoma ', i+1, ': ', k)
		operandos=[]
		for j in range(2**profundidad): operandos+=[random.choice((0, 1))]											#Prepara lista de terminales
		x=inferiorX
		while(x<=superiorX):																	#Recorre rango de variable independiente
			resultadoFuncion=((-2.34**3)-(-0.11*x/2))+23.45													#Evalua funcion
			#print('\n-Resultado de funcion: '+str(resultadoFuncion))
			nodos=pesosCromosoma[:]
			for j in range(2**profundidad):															#Genera lista de terminales a evaluar
				if(operandos[j]==0): operandos[j]=x
				else: operandos[j]=k
			entrada=operandos[:]
			resultadoCromosoma=evaluarArbolAlgebraico(nodos, entrada, 0, profundidad)									#Evalua cromosoma
			#print('-Resultado de cromosoma: '+str(resultadoCromosoma))
			resultadosCromosoma+=[resultadoCromosoma]
			erroresCromosoma+=[abs(resultadoFuncion-resultadoCromosoma)]											#Calcula error absoluto
			#print('Errores de cromosoma: '+str(erroresCromosoma))
			x=round(x+0.1, 1)
		resultados+=[resultadosCromosoma]
		errores+=[erroresCromosoma]																#Calcula utilidad de cromosoma
		utilidades+=[sum(erroresCromosoma)]
	#print('\nResultados de cromosomas: ')
	#for i in range(len(resultados)): print('-Cromosoma ', i+1, ': ', resultados[i])
	#print('\nErrores de cromosomas: ')
	#for i in range(len(errores)): print('-Cromosoma ', i+1, ': ', errores[i])
	#print('\nError de cromosomas: ')
	#for i in range(len(utilidades)): print('-Cromosoma ', i+1, ': ', utilidades[i])
	cromosomaElitista, utilidadElitistaActual=mejorar(cromosomas, utilidades, opcionSeleccion, cromosomaElitista, utilidadElitistaAnterior)	#Implementa elitismo
	aptitud=sum(utilidades)
	#print('\nUtilidad de la poblacion: ', aptitud)
	aptitudes=[]
	for i in range(len(utilidades)): aptitudes+=[utilidades[i]/aptitud]
	return aptitudes, cromosomaElitista, utilidadElitistaActual, aptitud

def generarPoblacion(tamanoCromosomas, tamanoPoblacion):
	cromosomas=[]
	if(tamanoPoblacion>1):
		for i in range(tamanoPoblacion):
			cromosoma=[]
			for j in range(tamanoCromosoma): cromosoma+=[random.choice((0, 1))]
			cromosomas+=[cromosoma]
		#mostrarCromosomas(cromosomas)
		return cromosomas
	else: print('\nError, introduciste un tamaño de población de cromosomas menor o igual a 1.')

numeros4=[[0, 0], [0, 1], [1, 0], [1, 1]]
numeros8=[[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
numeros16=[[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]	#Numeros binarios

cromosomas=generarPoblacion(tamanoCromosoma, tamanoPoblacion)
aptitudes, cromosomaElitista, utilidadElitista, aptitud=evaluarRegresion(cromosomas, inferiorX, superiorX, profundidad, None, numeros16, opcionSeleccion, None, None)
#aptitudes, cromosomaElitista, utilidadElitista, aptitud=evaluarParidad(cromosomas, profundidad, numeros4, opcionSeleccion, None, None)
for j in range(generaciones):
	cromosomas=seleccionar(cromosomas, aptitudes, opcionSeleccion)
	cromosomas=cruzar(cromosomas, probabilidadCruza)
	cromosomas=mutar(cromosomas, probabilidadMutacion)
	aptitudes, cromosomaElitista, utilidadElitista, aptitud=evaluarRegresion(cromosomas, inferiorX, superiorX, profundidad, None, numeros16, opcionSeleccion, cromosomaElitista, utilidadElitista)
	#aptitudes, cromosomaElitista, utilidadElitista, aptitud=evaluarParidad(cromosomas, profundidad, numeros4, opcionSeleccion, cromosomaElitista, utilidadElitista)
