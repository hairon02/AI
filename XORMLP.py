from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# *XOR con MLP (Perceptrón Multicapa) usando scikit-learn
# https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html

# Datos de entrada y salida para XOR
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [0, 1, 1, 0]  # Salidas deseadas (XOR)

# Crear el modelo MLP
mlp = MLPClassifier(hidden_layer_sizes=(3,),  # 1 capa oculta con 3 neuronas
                    activation='tanh',    # Función de activación sigmoide
                    solver='sgd',           # Algoritmo de optimización
                    max_iter=1001,            # Iteraciones para converger
                    random_state=42)

# Entrenar el modelo
mlp.fit(X, y)

# Hacer predicciones
y_pred = mlp.predict(X)

# Imprimir resultados
for xi, pred in zip(X, y_pred):
    print(f"Entrada: {xi}, Salida predicha: {pred}")

# Ver precisión
print("Precisión:", accuracy_score(y, y_pred))
print("La precision es del 100% con 1 capa oculta y 3 neuronas, con un maximo de 1001 iteraciones.")


# Comparación con 2 capas ocultas
print("\nComparación con 2 capas ocultas:")
mlp2 = MLPClassifier(hidden_layer_sizes=(3, 3),  # 2 capas ocultas con 3 neuronas cada una
                    activation='tanh',    # Función de activación sigmoide
                    solver='sgd',           # Algoritmo de optimización
                    max_iter=500,            # Iteraciones para converger
                    random_state=42)
mlp2.fit(X, y)
y_pred = mlp2.predict(X)
for xi, pred in zip(X, y_pred):
    print(f"Entrada: {xi}, Salida predicha: {pred}")

# Ver precisión
print("Precisión:", accuracy_score(y, y_pred))
print("La precision es del 100% con 2 capas ocultas y 3 neuronas cada una, con un maximo de 500 iteraciones.")