import csv
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Leer títulos
titulos = []
with open('pricerunner_aggregate.csv', 'r', encoding='utf-8') as archivo:
    lector = csv.reader(archivo)
    next(lector)  # saltar encabezado
    for fila in lector:
        try:
            titulo = fila[1].strip()
            if titulo:
                titulos.append(titulo)
        except IndexError:
            continue

# Dividir en entrenamiento y prueba
titulos_entrenamiento, titulos_prueba = train_test_split(titulos, test_size=0.2, random_state=42)

# Vectorizar con TF-IDF
vectorizador = TfidfVectorizer(stop_words='english')
X_entrenamiento = vectorizador.fit_transform(titulos_entrenamiento)
X_prueba = vectorizador.transform(titulos_prueba)

# Aplicar KMeans
k = 10
modelo = KMeans(n_clusters=k, n_init="auto")
modelo.fit(X_entrenamiento)

# Predecir algunos ejemplos
print("\n--- Ejemplos de predicción (15 títulos de prueba) ---")
for i in range(15):
    titulo = titulos_prueba[i]
    grupo = modelo.predict(vectorizador.transform([titulo]))[0]
    print(f"Título: '{titulo}' -> Grupo: {grupo}")

# Mostrar términos más representativos por centroide
print("\n--- Palabras más representativas(Centroides) por grupo ---")
palabras = vectorizador.get_feature_names_out()
orden_centroides = modelo.cluster_centers_.argsort(axis=1)[:, ::-1]

for i in range(k):
    top_palabras = [palabras[indice] for indice in orden_centroides[i][:10]]
    print(f"Grupo {i}: {', '.join(top_palabras)}")
