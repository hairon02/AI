# logica/03-GeneraConexionesFiguras.py

import json
import networkx as nx
from shapely.geometry import Polygon, LineString, MultiPolygon, Point
from shapely.ops import unary_union
from math import atan2


# === CONFIGURACIÓN ===
def GeneraConnFig():
    ARCHIVO_ENTRADA = "logica/grafo_figuras.json"
    ARCHIVO_SALIDA = "logica/grafo_sin_cruce.json"

    DISTANCIA_FUSION = 15
    
    # --- NUEVAS CONSTANTES ---
    # Dimensiones del área de juego donde se pueden generar nodos.
    # Coincide con el área del editor en editorEscenarios.py.
    ANCHO_ESCENARIO = 1000
    ALTO_ESCENARIO = 720

    # === CARGAR GRAFO ORIGINAL ===
    with open(ARCHIVO_ENTRADA) as f:
        data = json.load(f)

    grafo_original = data["grafo"]
    coordenadas = data["coordenadas"]

    # === DETECTAR FIGURAS (sin cambios) ===
    G_figuras = nx.Graph()
    for nodo, vecinos in grafo_original.items():
        if nodo not in ["Robot", "Bandera"]:
            for vecino in vecinos:
                if vecino not in ["Robot", "Bandera"]:
                    G_figuras.add_edge(nodo, vecino)
    componentes = list(nx.connected_components(G_figuras))

    # === CONSTRUIR POLÍGONOS (sin cambios) ===
    poligonos_originales = []
    figura_por_nodo = {}
    for i, comp in enumerate(componentes):
        nodos = list(comp)
        coords = [tuple(coordenadas[n]) for n in nodos]
        if len(coords) >= 3:
            cx = sum(x for x, y in coords) / len(coords)
            cy = sum(y for x, y in coords) / len(coords)
            coords_ordenadas = sorted(coords, key=lambda p: atan2(p[1] - cy, p[0] - cx))
            poligono = Polygon(coords_ordenadas)
            poligonos_originales.append(poligono)
            for n in comp:
                figura_por_nodo[n] = i

    # === FUSIÓN DE OBSTÁCULOS (sin cambios) ===
    poligonos_inflados = [p.buffer(DISTANCIA_FUSION) for p in poligonos_originales]
    geometria_unificada = unary_union(poligonos_inflados)
    geometria_final = geometria_unificada.buffer(-DISTANCIA_FUSION)
    poligonos_fusionados = []
    if isinstance(geometria_final, MultiPolygon):
        poligonos_fusionados.extend(geometria_final.geoms)
    elif isinstance(geometria_final, Polygon):
        poligonos_fusionados.append(geometria_final)
    print(f"Se fusionaron {len(poligonos_originales)} obstáculos en {len(poligonos_fusionados)} grupos.")

    # === FILTRAR NODOS INVÁLIDOS (LÓGICA ACTUALIZADA) ===
    # Ahora también se descartan los nodos fuera de los límites del escenario.
    nodos_validos = list(data["coordenadas"].keys())
    coordenadas = data["coordenadas"] # Usamos directamente las coordenadas de data
    nodos_a_eliminar = set()

    nodo_inicio_nombre = data.get("inicio")
    nodo_meta_nombre = data.get("meta")

    for nodo_id in nodos_validos:
        x, y = coordenadas[nodo_id]
        # --- NUEVA CONDICIÓN DE EXCEPCIÓN ---
        # Si el nodo es el de inicio o el de meta, no se valida y se considera siempre correcto.
        if nodo_id == nodo_inicio_nombre or nodo_id == nodo_meta_nombre:
            continue

        # --- NUEVA COMPROBACIÓN ---
        # Condición 1: ¿El nodo está fuera de los límites del escenario?
        if not (0 <= x <= ANCHO_ESCENARIO and 0 <= y <= ALTO_ESCENARIO):
            print(f"⚠️  Vértice '{nodo_id}' descartado por estar fuera del escenario.")
            nodos_a_eliminar.add(nodo_id)
            continue  # Si ya está fuera, no es necesario comprobar si está en un obstáculo

        # Condición 2: ¿El nodo está dentro de un obstáculo?
        punto_nodo = Point(x, y)
        for obstaculo in poligonos_fusionados:
            if obstaculo.contains(punto_nodo):
                print(f"⚠️  Vértice '{nodo_id}' descartado por estar dentro de un obstáculo.")
                nodos_a_eliminar.add(nodo_id)
                break 
    
    # Limpiamos el grafo y las coordenadas de los nodos eliminados
    for nodo_id in nodos_a_eliminar:
        if nodo_id in nodos_validos:
             nodos_validos.remove(nodo_id)
        coordenadas.pop(nodo_id, None)
        grafo_original.pop(nodo_id, None)
        for nodo_vecino in grafo_original:
            if nodo_id in grafo_original[nodo_vecino]:
                grafo_original[nodo_vecino].remove(nodo_id)
    
    # === GENERAR CONEXIONES (sin cambios) ===
    nuevo_grafo = {n: list(v) for n, v in grafo_original.items() if n in nodos_validos}
    for i in range(len(nodos_validos)):
        for j in range(i + 1, len(nodos_validos)):
            a, b = nodos_validos[i], nodos_validos[j]
            fig_a = figura_por_nodo.get(a)
            fig_b = figura_por_nodo.get(b)
            if (fig_a is not None and fig_b is not None and fig_a == fig_b):
                continue
            linea = LineString([tuple(coordenadas[a]), tuple(coordenadas[b])])
            cruza_figura = False
            for poly in poligonos_fusionados:
                if linea.intersects(poly) and not linea.touches(poly):
                    cruza_figura = True
                    break
            if not cruza_figura:
                if b not in nuevo_grafo.setdefault(a, []):
                    nuevo_grafo[a].append(b)
                if a not in nuevo_grafo.setdefault(b, []):
                    nuevo_grafo[b].append(a)

    # === GUARDAR GRAFO ACTUALIZADO (sin cambios) ===
    inicio_final = data.get("inicio") if data.get("inicio") in nodos_validos else None
    meta_final = data.get("meta") if data.get("meta") in nodos_validos else None
    nuevo_json = {
        "grafo": nuevo_grafo,
        "coordenadas": coordenadas,
        "inicio": inicio_final,
        "meta": meta_final
    }
    with open(ARCHIVO_SALIDA, "w") as f:
        json.dump(nuevo_json, f, indent=4)
    print(f"Grafo con obstáculos fusionados y nodos validados guardado en {ARCHIVO_SALIDA}")