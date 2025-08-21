import csv
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Rutas
archivo = 'household_power_consumption.txt'

# Inicializamos listas
X = []
y = []

# Leer archivo línea por línea
with open(archivo, 'r') as f:
    lector = csv.reader(f, delimiter=';')
    next(lector)  # Saltar encabezado

    for fila in lector:
        try:
            global_active_power = float(fila[2].replace(',', '.'))  # Columna 3
            global_intensity = float(fila[5].replace(',', '.'))     # Columna 6

            if '?' in (fila[2], fila[5]):
                continue
            y.append(global_active_power)  # variable dependiente
            X.append([global_intensity])   # variable independiente


        except (ValueError, IndexError):
            continue  # Ignorar filas con datos faltantes

# Convertimos a arreglos NumPy
X = np.array(X)
y = np.array(y)

# Dividir en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Crear modelo y entrenar
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Obtener coeficientes
m = modelo.coef_[0]
b = modelo.intercept_

# Mostrar resultados
ecuacion = f'y = {m}x + {b}' if b >= 0 else f'y = {m}x - {abs(b)}'
print(f"Coeficiente de determinación (R²): {modelo.score(X_test, y_test)}")
print(f"Pendiente (m): {m}")
print(f"Intercepto (b): {b}")
print("\nEcuación de la regresión lineal:")
print(ecuacion)

# Predicciones
"""
valores_prediccion = np.array([[5], [10], [15], [20], [25], [30], [35], [40], [45], [50]])
predicciones = modelo.predict(valores_prediccion)

print("\nPredicciones para Intensidades 5, 10, 15, 20, 25 30 35 40 45 50:")
for i, val in enumerate(valores_prediccion.flatten()):
    print(f"Intensidad {val} A → Potencia estimada: {predicciones[i]:.4f} kW")
"""

print("\nPredicciones con 15 valores reales del conjunto de prueba:")
for i in range(15):
    intensidad_real = X_test[i][0]
    potencia_real = y_test[i]
    potencia_predicha = modelo.predict([[intensidad_real]])[0]
    print(f"{i+1:02d}. Intensidad real: {intensidad_real} A | Potencia real: {potencia_real} kW → Potencia estimada: {potencia_predicha} kW | Error de prediccion: {abs(potencia_real - potencia_predicha)} kW")
