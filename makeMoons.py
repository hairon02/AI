from sklearn.datasets import make_moons
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


"""
Clasificación de datos no lineales con MLP (Perceptrón Multicapa) usando scikit-learn
https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_moons.html

make_moons es una función de Scikit-learn que genera datos sintéticos en forma de dos arcos o medias lunas entrelazadas. 
Se usa mucho para probar clasificadores que manejan datos no linealmente separables.


"""
# Parámetro: número de muestras para entrenamiento
N = 100

# Crear el conjunto de entrenamiento
X_train, y_train = make_moons(n_samples=N, noise=0.2, random_state=42)

# Crear un conjunto de prueba distinto (2N muestras)
X_test, y_test = make_moons(n_samples=2*N, noise=0.2, random_state=1)

# Crear el modelo MLP
mlp = MLPClassifier(hidden_layer_sizes=(10, 10),   # 2 capas ocultas: 10 y 10 neuronas
                    activation='tanh',            # Función de activación tangente hiperbólica
                    solver='sgd',                 # Descenso de gradiente estocástico
                    learning_rate_init=0.01,      # Tasa de aprendizaje
                    max_iter=1000,
                    random_state=42)

# Entrenar el modelo
mlp.fit(X_train, y_train)

# Evaluar el modelo
y_pred = mlp.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Precisión en el conjunto de prueba:", accuracy)

# Visualizar la clasificación
plt.figure(figsize=(8, 6))
plt.scatter(X_test[:, 0], # Coordenada x de cada punto (primera columna del array X_test)
            X_test[:, 1], 
            c=y_pred, # El color del punto depende de la clase predicha (0 o 1)
            cmap='coolwarm', # Mapa de colores (azul para una clase, rojo para otra)
            #edgecolor='k', # Borde negro para los puntos
            marker='o' # Tipo de marcador circular
)
plt.title("Clasificación del conjunto de prueba")
plt.xlabel("X1")
plt.ylabel("X2")
plt.show()
