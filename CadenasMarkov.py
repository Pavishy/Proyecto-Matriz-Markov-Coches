import numpy as n

T = [0.6,0.2,0.2],[0.3,0.4,0.3],[0.1,0.4,0.5]

P_inicial = [0.7,0.2,0.1]

matrizT = n.array(T)
matriz_P0 = n.array(P_inicial)

print(matrizT)
print()
print(matriz_P0)

print("P1: ")
P1 = matriz_P0.dot(matrizT)
print(P1)

print("P2: ")
P2 = P1.dot(matrizT)
print(P2)

estadoDeseado = int(input("Ingresa el estado que se desea: "))
print("Estado buscado: " + str(estadoDeseado))

estadoActual = matriz_P0
for i in range(estadoDeseado):
    estadoActual = estadoActual.dot(matrizT)
    print ("P" +str(i+1)+": "+ str(estadoActual))

print("Resultado: (P"+str(estadoDeseado)+"): ")
print(estadoActual)

#CODIGO DE COCHES