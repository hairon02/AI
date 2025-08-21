import pygame
import sys
import subprocess
import json
import os
import math # <--- IMPORTANTE: Añadir math para la rotación
from logica.utils import cargar_coordenadas, traducir_camino_a_coordenadas
# ... (resto de tus imports)
from algoritmos import BusqAmplitud
from algoritmos import BusqProfundidad
from algoritmos import BusqProfIterativa
from algoritmos import busqueda_costo_uniforme
from algoritmos import busqueda_avara
from algoritmos import busqueda_a_estrella
import editorEscenarios


def menu():
    pygame.init()
    camino_a_dibujar = None

    # ... (Clase ObjetoJuego y cargar_escenario_juego se mantienen igual)
    class ObjetoJuego(pygame.sprite.Sprite):
        def __init__(self, pos, image, angle):
            super().__init__()
            self.original_image = image
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=pos)
            

    def cargar_escenario_juego(offset):
        objetos_del_juego = pygame.sprite.Group()
        imagenes_cargadas = {}
        offset_x, offset_y = offset
        if not os.path.exists('interfaz/escenario.json'):
            print("⚠ No se encontró el archivo 'escenario.json'. El escenario estará vacío.")
            return objetos_del_juego
        with open('interfaz/escenario.json', 'r') as f:
            data_escenario = json.load(f)
        for item_data in data_escenario:
            path = item_data['path']
            if path not in imagenes_cargadas:
                try:
                    imagenes_cargadas[path] = pygame.image.load(path).convert_alpha()
                except pygame.error:
                    print(f"⚠ No se pudo cargar la imagen: {path}. Se omitirá este objeto.")
                    continue
            imagen = imagenes_cargadas[path]
            pos_guardada = item_data['pos']
            angulo_guardado = item_data['angle']
            nuevo_x = pos_guardada[0] + offset_x
            nuevo_y = pos_guardada[1] + offset_y
            objeto = ObjetoJuego((nuevo_x, nuevo_y), imagen, angulo_guardado)
            objetos_del_juego.add(objeto)
        print(f"✔ Escenario cargado con {len(objetos_del_juego)} objetos.")
        return objetos_del_juego

    # ... (Configuración de dimensiones, colores y fuentes se mantiene igual)
    WIDTH, HEIGHT = 1200, 860
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menú Principal - Pygame")
    BG_COLOR = (29, 29, 47)
    WHITE = (255, 255, 255)
    GRAY = (58, 58, 90)
    GREEN = (60, 176, 67)
    RED = (198, 64, 64)
    LIGHT_GRAY = (100, 100, 140)
    DISABLED_GRAY = (80, 80, 110)
    HOVER_GRAY = (75, 75, 110)
    HOVER_GREEN = (80, 200, 90)
    HOVER_RED = (210, 80, 80)
    BASE_PATH = os.path.dirname(__file__)
    IMG_PATH = os.path.join(BASE_PATH, "interfaz", "img", "fondo_menu.png")
    camino = []
    font = pygame.font.SysFont("arial", 16)
    btn_width = 170
    btn_height = 40
    GAP_X = 40
    TOP_MARGIN = 45
    group_width = btn_width * 4 + GAP_X * 3 + 120
    start_x = (WIDTH - group_width) // 2
    btn_back = pygame.Rect(start_x, TOP_MARGIN, btn_width, btn_height)
    combo_box = pygame.Rect(btn_back.right + GAP_X, TOP_MARGIN, btn_width + 120, btn_height)
    btn_start = pygame.Rect(combo_box.right + GAP_X, TOP_MARGIN, btn_width, btn_height)
    btn_exit = pygame.Rect(btn_start.right + GAP_X, TOP_MARGIN, btn_width, btn_height)
    algoritmos = ["Búsqueda en Amplitud", "Búsqueda en Profundidad", "Búsqueda por Profundización Iterativa", "Búsqueda de Costo Uniforme", "Búsqueda A*", "Búsqueda Avara"]
    selected_index = -1
    combo_open = False
    # --- Variables de estado de la interfaz (MODIFICADAS) ---
    font_info = pygame.font.SysFont("arial", 20, bold=True)
    font_pesos = pygame.font.SysFont("arial", 14, bold=True)
    mensaje_pantalla = "" # Para mostrar "No se encontró camino"
    costo_camino = None # Para mostrar el costo total
    mostrar_pesos = False # Flag para dibujar los pesos de las aristas
    
    # --- Variables de animación MODIFICADAS ---
    segmento_actual = 0
    progreso_segmento = 0.0
    velocidad_animacion = 0.02  # Ajustada para un movimiento más fluido por frame
    animacion_terminada = False # <-- NUEVA VARIABLE DE ESTADO
    
    # Cargar las dos imágenes del robot (se mantiene igual)
    robot_image_1 = pygame.image.load("interfaz/img/robot1.png").convert_alpha()
    robot_image_2 = pygame.image.load("interfaz/img/robot2.png").convert_alpha()
    frame_counter = 0
    image_toggle = True

    def get_combo_items_rects():
        return [pygame.Rect(combo_box.x, combo_box.bottom + 5 + i * 30, combo_box.width, 30)
                for i in range(len(algoritmos))]

    # Carga de recursos del escenario (se mantiene igual)
    juego_area = pygame.Rect(60, 120, 1000, 720)
    try:
        fondo_imagen = pygame.image.load(IMG_PATH).convert()
        fondo_ajustado = pygame.transform.scale(fondo_imagen, (juego_area.width, juego_area.height))
    except Exception as e:
        print("⚠ No se pudo cargar fondo.PNG:", e)
        fondo_ajustado = None
    escenario_sprites = cargar_escenario_juego(juego_area.topleft)

    running = True
    clock = pygame.time.Clock() # <--- Añadir un reloj para controlar FPS

    while running:
        # Controlar la velocidad del bucle
        clock.tick(60) # Limitar a 60 FPS

        screen.fill(BG_COLOR)

        if fondo_ajustado:
            screen.blit(fondo_ajustado, juego_area.topleft)
        else:
            pygame.draw.rect(screen, (20, 20, 30), juego_area)
        
        escenario_sprites.draw(screen)

        if camino_a_dibujar and len(camino_a_dibujar) > 1:
            # 1. Dibuja las líneas amarillas del camino
            pygame.draw.lines(screen, (255, 255, 0), False, camino_a_dibujar, 5)

            # --- NUEVA LÓGICA PARA REMARCAR NODOS ---
            # 2. Dibuja un punto verde en cada nodo del camino
            color_nodo = (50, 255, 50)  # Verde brillante
            for pos_nodo in camino_a_dibujar:
                pygame.draw.circle(screen, color_nodo, pos_nodo, 8)  # Círculo de 8px de radio
            # --- FIN DE LA NUEVA LÓGICA ---

            # 3. Dibuja los pesos de las aristas si corresponde (sin cambios)
            if mostrar_pesos and todas_las_coords:
                for i in range(len(camino) - 1):
                    nodo_a_id = camino[i]
                    nodo_b_id = camino[i+1]

                    coord_a = todas_las_coords.get(nodo_a_id)
                    coord_b = todas_las_coords.get(nodo_b_id)
                    if coord_a and coord_b:
                        dist = math.dist(coord_a, coord_b)
                        
                        screen_a = camino_a_dibujar[i]
                        screen_b = camino_a_dibujar[i+1]
                        mid_x = (screen_a[0] + screen_b[0]) / 2
                        mid_y = (screen_a[1] + screen_b[1]) / 2
                        
                        texto_peso = font_pesos.render(str(round(dist)), True, (255, 0, 128))
                        text_rect = texto_peso.get_rect(center=(mid_x, mid_y - 15))
                        pygame.draw.rect(screen, (0, 0, 0, 150), text_rect.inflate(4, 4))
                        screen.blit(texto_peso, text_rect)


        # --- SECCIÓN DE ANIMACIÓN DEL ROBOT (TOTALMENTE MODIFICADA) ---
        if camino_a_dibujar and len(camino_a_dibujar) > 1:
            pos_robot_actual = (0, 0)
            robot_rotado = robot_image_1

            if not animacion_terminada:
                # Puntos del segmento actual
                A = camino_a_dibujar[segmento_actual]
                B = camino_a_dibujar[segmento_actual + 1]

                # Calcular la posición actual usando interpolación lineal (Lerp)
                P_x = A[0] + (B[0] - A[0]) * progreso_segmento
                P_y = A[1] + (B[1] - A[1]) * progreso_segmento
                pos_robot_actual = (P_x, P_y)

                # Calcular ángulo de rotación
                # El sprite mira a la derecha (0 grados), así que calculamos el ángulo del vector de movimiento
                dx = B[0] - A[0]
                dy = B[1] - A[1]
                angulo = math.degrees(math.atan2(-dy, dx)) # Negativo en 'dy' por el eje Y invertido de Pygame

                # Alternar imagen para simular caminata
                if frame_counter % 20 == 0: # Cambiar imagen cada 20 frames
                    image_toggle = not image_toggle
                
                robot_base = robot_image_1 if image_toggle else robot_image_2
                robot_rotado = pygame.transform.rotate(robot_base, angulo)

                # Actualizar progreso
                progreso_segmento += velocidad_animacion
                if progreso_segmento >= 1.0:
                    progreso_segmento = 0.0
                    segmento_actual += 1

                    # Comprobar si hemos llegado al final del camino
                    if segmento_actual >= len(camino_a_dibujar) - 1:
                        animacion_terminada = True
            
            if animacion_terminada:
                # Si la animación terminó, el robot se queda en el punto final
                pos_robot_actual = camino_a_dibujar[-1]
                # Para que mire en la última dirección que tuvo
                A = camino_a_dibujar[-2]
                B = camino_a_dibujar[-1]
                dx = B[0] - A[0]
                dy = B[1] - A[1]
                angulo = math.degrees(math.atan2(-dy, dx))
                robot_rotado = pygame.transform.rotate(robot_image_1, angulo)

            # Dibujar el robot
            robot_rect = robot_rotado.get_rect(center=pos_robot_actual)
            screen.blit(robot_rotado, robot_rect)

            frame_counter += 1

        # --- Interfaz de Usuario (sin cambios) ---
        mouse_pos = pygame.mouse.get_pos()
        combo_items_rects = get_combo_items_rects()
        back_hover = btn_back.collidepoint(mouse_pos)
        pygame.draw.rect(screen, HOVER_GRAY if back_hover else GRAY, btn_back)
        text_back = font.render("← editar entorno", True, WHITE)
        screen.blit(text_back, text_back.get_rect(center=btn_back.center))
        pygame.draw.rect(screen, GRAY, combo_box)
        texto = "selecciona el algoritmo de búsqueda" if selected_index == -1 else algoritmos[selected_index]
        text_combo = font.render(texto, True, WHITE)
        screen.blit(text_combo, text_combo.get_rect(center=combo_box.center))
        start_hover = btn_start.collidepoint(mouse_pos)
        color_start = HOVER_GREEN if start_hover else GREEN if selected_index != -1 else DISABLED_GRAY
        pygame.draw.rect(screen, color_start, btn_start)
        text_start = font.render("iniciar", True, WHITE)
        screen.blit(text_start, text_start.get_rect(center=btn_start.center))
        exit_hover = btn_exit.collidepoint(mouse_pos)
        pygame.draw.rect(screen, HOVER_RED if exit_hover else RED, btn_exit)
        text_exit = font.render("salir", True, WHITE)
        screen.blit(text_exit, text_exit.get_rect(center=btn_exit.center))
        if combo_open:
            for i, rect in enumerate(combo_items_rects):
                item_hover = rect.collidepoint(mouse_pos)
                pygame.draw.rect(screen, HOVER_GRAY if item_hover else LIGHT_GRAY, rect)
                text_item = font.render(algoritmos[i], True, WHITE)
                screen.blit(text_item, (rect.x + 10, rect.y + 6))

        if mensaje_pantalla:
            texto_surf = font_info.render(mensaje_pantalla, True, (255, 80, 80))
            texto_rect = texto_surf.get_rect(center=(juego_area.centerx, juego_area.top + 30))
            screen.blit(texto_surf, texto_rect)

        # Dibujar el costo total del camino
        if costo_camino is not None:
            texto_costo = f"Costo total del camino: {round(costo_camino)}"
            texto_surf = font_info.render(texto_costo, True, (80, 255, 80))
            texto_rect = texto_surf.get_rect(topright=(juego_area.right - 20, juego_area.top + 20))
            screen.blit(texto_surf, texto_rect)

        # --- Bucle de eventos (con reinicio de animación) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if btn_exit.collidepoint(mx, my):
                    # ... (código de salida se mantiene igual)
                    try:
                        if os.path.exists('interfaz/escenario.json'):
                            os.remove('interfaz/escenario.json')
                            print("Archivo 'escenario.json' eliminado.")
                    except OSError as e:
                        print(f"Error al eliminar el archivo: {e}")
                    running = False
                elif btn_back.collidepoint(mx, my):
                    # ... (código de ir atrás se mantiene igual)
                    try:
                        editorEscenarios.Editor()
                        pygame.quit()
                        sys.exit()
                    except Exception as e:
                        print("Error al abrir editorEscenarios.py:", e)
                elif btn_start.collidepoint(mx, my) :
                    if selected_index != -1:
                        print(f"Iniciando algoritmo: {algoritmos[selected_index]}")
                        
                        # --- REINICIO DE ESTADO ---
                        camino_a_dibujar = None
                        camino = None # <--- importante
                        costo_camino = None
                        mensaje_pantalla = ""
                        mostrar_pesos = selected_index >= 3 # Activar para Costo Uniforme, A* y Avara

                        # Lógica para llamar a los algoritmos (MODIFICADA para capturar costo)
                        if selected_index == 0: camino = BusqAmplitud.Amplitud()
                        elif selected_index == 1: camino = BusqProfundidad.Profundidad()
                        elif selected_index == 2: camino = BusqProfIterativa.ProfundidadI()
                        elif selected_index == 3: camino, costo_camino = busqueda_costo_uniforme.Uniforme()
                        elif selected_index == 4: camino, costo_camino = busqueda_a_estrella.estrella()
                        elif selected_index == 5: camino, costo_camino = busqueda_avara.Avara()

                        if camino:
                            # Si hay camino, reinicia la animación
                            animacion_terminada = False
                            segmento_actual = 0
                            progreso_segmento = 0.0
                            # Y traduce las coordenadas para dibujarlo
                            todas_las_coords = cargar_coordenadas("logica/datos_completos.txt")
                            offset = juego_area.topleft
                            camino_a_dibujar = traducir_camino_a_coordenadas(camino, todas_las_coords, offset)
                        else:
                            # Si no hay camino, establece el mensaje
                            mensaje_pantalla = "No se encontró un camino."
                    else:
                        mensaje_pantalla = "Por favor, seleccione un algoritmo"
                # ... (resto de eventos de combobox sin cambios)
                elif combo_box.collidepoint(mx, my):
                    combo_open = not combo_open

                elif combo_open:
                    for i, rect in enumerate(combo_items_rects):
                        if rect.collidepoint(mx, my):
                            selected_index = i
                            combo_open = False
                            break
                    else:
                        combo_open = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()