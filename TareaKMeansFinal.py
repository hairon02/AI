# Para ejecutarlo: python3 .\TareaKMeansFinal.py
# pip install pandas scikit-learn

import zipfile
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1) Ruta del fichero ZIP (misma carpeta que este .py)
ruta_zip = 'online+retail.zip'

# 2) Leer el CSV desde el ZIP
with zipfile.ZipFile(ruta_zip) as z:
    # Asumimos que el archivo principal es 'Online Retail.csv'
    nombre_archivo = [f for f in z.namelist() if f.endswith('.csv')][0]
    df = pd.read_csv(z.open(nombre_archivo), encoding='ISO-8859-1')

# 3) Preprocesamiento básico
print(f"Dimensiones originales: {df.shape}")
# Eliminamos filas con valores nulos
df = df.dropna()
# Filtramos solo los datos positivos de cantidad y precio
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
# Creamos una columna de TotalPrice = Quantity * UnitPrice
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Seleccionamos solo columnas numéricas útiles
X = df[['Quantity', 'UnitPrice', 'TotalPrice']]

# Normalizamos los datos para el KMeans
scaler = StandardScaler()
X_normalizado = scaler.fit_transform(X)

# 4) División 80/20
X_entreno, X_prueba = train_test_split(X_normalizado, test_size=0.2, random_state=42)

# 5) KMeans con 5 grupos (puedes ajustar este valor)
kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(X_entreno)

# 6) Predicción de grupos
y_pred = kmeans.predict(X_prueba)

# 7) Resultados
print("\n=== Agrupamiento K-Means ===")
print(f"Total muestras en prueba: {X_prueba.shape[0]}")
print(f"Centroides de los clústeres:\n{kmeans.cluster_centers_}")

# Mostrar algunas predicciones
df_resultados = pd.DataFrame(X_prueba, columns=['Quantity', 'UnitPrice', 'TotalPrice'])
df_resultados['Grupo_Predicho'] = y_pred
print("\nPrimeras 10 predicciones de grupo:")
print(df_resultados.head(10))
