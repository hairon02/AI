import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Cargar el archivo CSV
df = pd.read_csv("household_power_consumption.txt", sep=';', 
                 na_values='?', low_memory=False)

# Convertir a valores numéricos y eliminar filas con valores faltantes
df[['Global_active_power', 'Global_intensity']] = df[['Global_active_power', 'Global_intensity']].apply(pd.to_numeric, errors='coerce')
df.dropna(subset=['Global_active_power', 'Global_intensity'], inplace=True)

# Seleccionar variable independiente (X) y dependiente (y)
X = df[['Global_intensity']].values  # variable predictora
y = df[['Global_active_power']].values  # variable objetivo

# Dividir en conjuntos de entrenamiento y prueba (opcional)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Crear y entrenar el modelo
reg = LinearRegression().fit(X_train, y_train)

# Obtener coeficientes
m = reg.coef_[0][0]  # Pendiente
b = reg.intercept_[0]  # Intercepto

# Ecuación de la recta
ecuacion = f'y = {m}x + {b}' if b >= 0 else f'y = {m}x - {abs(b)}'
#ecuacion = f'y = {m:.2f}x + {b:.2f}' if b >= 0 else f'y = {m:.2f}x - {abs(b):.2f}'

# Imprimir resultados
print(f"Coeficiente de determinación (R²): {reg.score(X_test, y_test)}")
print(f"Pendiente (m): {m:.2f}")
print(f"Intercepto (b): {b:.2f}")
print("\nEcuación de la regresión lineal:")
print(ecuacion)

# Hacer predicciones
valores_prediccion = np.array([[5], [10], [15], [20], [25]])
predicciones = reg.predict(valores_prediccion)
print("\nPredicciones para [5, 10, 15, 20, 25]:")
print(predicciones)
