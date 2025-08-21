import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[-1], [0], [1], [2], [3], [4]])
y = np.array([[-3], [-1], [1], [3], [5], [7]])

reg = LinearRegression().fit(X, y)

# Obtener coeficientes
m = reg.coef_[0][0]  # Pendiente (m)
b = reg.intercept_[0]  # Intercepto (b)

# Formatear la ecuación
ecuacion = f'y = {m:.2f}x + {b:.2f}' if b >= 0 else f'y = {m:.2f}x - {abs(b):.2f}'

# Imprimir resultados
print(f"Coeficiente de determinación (R²): {reg.score(X, y)}")
print(f"Pendiente (m): {m:.2f}")
print(f"Intercepto (b): {b:.2f}")
print("\nEcuación de la regresión lineal:")
print(ecuacion)
print("\nPredicciones para [5, 10, 15, 20, 25]:")
print(reg.predict(np.array([[5], [10], [15], [20], [25]])))