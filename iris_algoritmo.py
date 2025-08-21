import random

class MasCercanos:
    def __init__(self):
        datos1 = []
        archivo = open("iris.data", "r")
        while True:
            linea = str(archivo.readline())
            aux1 = linea.split(",")
            if linea == "" or linea == "\n":
                break
            datos1.append([[float(aux1[0]),float(aux1[1]),float(aux1[2]),float(aux1[3])],aux1[4].strip()])
        archivo.close()

        random.shuffle(datos1)
        self.datos = datos1[:120]
        self.tests = datos1[120:]
    
    def distancia_minkowski(self, vec1, vec2, p) -> float:
        dato1 : float = 0.0
        for i in range(4):
            dato1 = dato1 + abs(vec1[i] - vec2[i]) ** p
        suma = dato1 ** (1/p)
        return suma

        #return sum(abs(x - y) ** p for x, y in zip(vec1, vec2)) ** (1/p)
        
    def masCercanos(self, vector, k) -> str:
        distancias = []
        index: int = 0
        for dato in self.datos:
            distancias.append([index, self.distancia_minkowski(vector, dato[0], 2)])
            index = index+1
        distancias = sorted(distancias, key=lambda x: x[1])
        
        cerca = distancias[:k]
        cercanos = []
        for cer in cerca:
            cercanos.append(self.datos[cer[0]])

        clases = []
        for vect in cercanos:
            if clases==None or (any(sublista[0] == vect[1] for sublista in clases)==False):
                clases.append([vect[1],1])
            else:
                clases[next(i for i, sublista in enumerate(clases) if sublista[0] == vect[1])][1] +=1
        clases = sorted(clases, key=lambda x: x[1])
        return clases[0][0]
    
    def testing(self):
        k: int = 1
        while k < 100:
            verdad = []
            for dato in self.tests:
                aux1: str = self.masCercanos(dato[0],k)
                verdad.append(aux1 == dato[1])
            print("con k = ", k)
            print(verdad)
            print(sum(verdad), ", el porcentaje de exactitud es de ", (sum(verdad)*100)/30, "%")
            k +=3

a = MasCercanos()
a.testing()