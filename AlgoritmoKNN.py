# Algoritmo kNN

import random
import math

class VecinosMasCercanos:
    def __init__(self, ruta_archivo="iris.data", proporcion_entrenamiento=0.8, semilla=42):
        """
        Carga y divide el conjunto de datos en entrenamiento y prueba.
        """
        self.datos_entrenamiento = []
        self.datos_prueba = []

        datos_totales = []
        with open(ruta_archivo, "r") as archivo:
            for linea in archivo:
                if linea.strip() == "":
                    continue
                partes = linea.strip().split(",")
                caracteristicas = list(map(float, partes[:4]))
                etiqueta = partes[4]
                datos_totales.append((caracteristicas, etiqueta))
        
        # Mezclar aleatoriamente los datos
        #random.seed(semilla)
        random.shuffle(datos_totales)

        # Dividir en entrenamiento y prueba
        total = len(datos_totales) # 150
        division = int(total * proporcion_entrenamiento) # 120
        self.datos_entrenamiento = datos_totales[:division]
        self.datos_prueba = datos_totales[division:]

    def distancia_euclidiana(self, a, b):
        """
        Calcula la distancia euclidiana entre dos vectores.
        """
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))) # zip(a, b) = [(5.1, 5.0), (3.5, 3.3), (1.4, 1.4), (0.2, 0.2)] 

    def obtener_vecinos(self, vector_consulta, k):
        """
        Encuentra los k vecinos más cercanos al vector de consulta.
        """
        distancias = []
        for ejemplo_entrenamiento in self.datos_entrenamiento:
            distancia = self.distancia_euclidiana(vector_consulta, ejemplo_entrenamiento[0])
            distancias.append((distancia, ejemplo_entrenamiento[1])) # Se aguarda en una tupla la distancia y clase
        distancias.sort(key=lambda x: x[0]) # x[0] es la distancia de cada uno
        vecinos = distancias[:k]
        return [etiqueta for _, etiqueta in vecinos]

    def predecir(self, vector_consulta, k):
        """
        Predice la clase de un vector dado usando votación mayoritaria.
        """
        vecinos = self.obtener_vecinos(vector_consulta, k)
        conteo = {}
        for etiqueta in vecinos:
            conteo[etiqueta] = conteo.get(etiqueta, 0) + 1
        return max(conteo, key=conteo.get) # busca la etiqueta que tiene el valor más alto.



    def evaluar(self, k):
        """
        Evalúa el rendimiento del clasificador con k vecinos.
        """
        correctos = 0
        print(f"\nEvaluando con k = {k} vecinos")
        for xq, etiqueta_real in self.datos_prueba:
            prediccion = self.predecir(xq, k)
            es_correcta = prediccion == etiqueta_real
            if es_correcta:
                correctos += 1
            #print(f"xq = {xq} | Clase real: {etiqueta_real} | Clase predicha: {prediccion}")
        total = len(self.datos_prueba)
        exactitud = (correctos / total) * 100
        error = 100 - exactitud
        print(f"Predicciones correctas: {correctos} de {total}", end="\t")
        print(f"Exactitud: {exactitud:.2f}% | Error: {error:.2f}%")
        return exactitud

    def probar_varios_k(self, lista_k):
        """
        Prueba múltiples valores de k y muestra la exactitud para cada uno.
        """
        resultados = {}
        for k in lista_k:
            exactitud = self.evaluar(k)
            resultados[k] = exactitud
        mejor_k = max(resultados, key=resultados.get)
        print(f"\nMejor valor de k: {mejor_k} con una exactitud de {resultados[mejor_k]:.2f}%")
        return mejor_k, resultados


modelo = VecinosMasCercanos("iris.data")
modelo.probar_varios_k([1, 3, 5, 7, 9, 11, 21, 31, 51, 91, 115])
