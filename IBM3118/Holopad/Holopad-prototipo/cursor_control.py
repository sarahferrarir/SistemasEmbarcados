# Gerencia as ações do cursor (mover, clicar, rolar) e o estado do sistema.

import cv2
import pyautogui
import time
import config  # Importa o arquivo config.py inteiro
from utils import get_gesture_distance, get_left_click_distance

# --- Variáveis de Estado do Módulo ---
# (Não são mais 'global' no main.py, elas "vivem" dentro deste arquivo)
dragging = False
previous_point_c = (0.5, 0.5)  # Iniciar no centro
last_scroll_y = 0              # Guarda a posição Y anterior para o scroll
scroll_mode_active = False     # Controla a inicialização do modo scroll


def calculate_vector(hand_landmarks):
    """Calcula o vetor 5 -> 12 -> C, aplicando suavização e deadzone."""
    # Acessa e atualiza a variável 'previous_point_c' deste módulo
    global previous_point_c
    
    try:
        lm5 = hand_landmarks.landmark[5]
        lm12 = hand_landmarks.landmark[12]

        direction_x = lm12.x - lm5.x
        direction_y = lm12.y - lm5.y
        point_c_x = lm5.x + config.VECTOR_MULTIPLIER * direction_x
        point_c_y = lm5.y + config.VECTOR_MULTIPLIER * direction_y

        delta_x = abs(point_c_x - previous_point_c[0])
        delta_y = abs(point_c_y - previous_point_c[1])

        if delta_x < config.DEADZONE and delta_y < config.DEADZONE:
            point_c_x, point_c_y = previous_point_c

        smoothed_x = previous_point_c[0] + (point_c_x - previous_point_c[0]) * config.SENSITIVITY
        smoothed_y = previous_point_c[1] + (point_c_y - previous_point_c[1]) * config.SENSITIVITY

        previous_point_c = (smoothed_x, smoothed_y)

        lm5_px = (int(lm5.x * 640), int(lm5.y * 480))
        lm12_px = (int(lm12.x * 640), int(lm12.y * 480))
        point_c_px = (int(smoothed_x * 640), int(smoothed_y * 480))

        return lm5_px, lm12_px, point_c_px, (smoothed_x, smoothed_y)
    except Exception as e:
        print(f"⚠️ Erro em calculate_vector: {e}")
        return None, None, None, None

def handle_scrolling(frame, hand_landmarks):
    """Controla o scroll da página baseado no movimento Y da mão."""
    global last_scroll_y, scroll_mode_active

    current_y = hand_landmarks.landmark[12].y
    
    if not scroll_mode_active:
        last_scroll_y = current_y
        scroll_mode_active = True
        print("📜 Modo Scroll ATIVADO")
        return

    delta_y = current_y - last_scroll_y
    cv2.putText(frame, "SCROLL MODE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    if abs(delta_y) > config.SCROLL_DEADZONE:
        scroll_amount = int(-delta_y * 100 * config.SCROLL_SENSITIVITY)
        if scroll_amount != 0:
            pyautogui.scroll(scroll_amount)
            print(f"📜 Scrolling: {scroll_amount}")

    last_scroll_y = current_y

def handle_pointing(frame, hand_landmarks, mp_draw, mp_hands):
    """Gerencia Apontar, Congelar, Clicar (L/R) e Arrastar."""
    global dragging, scroll_mode_active
    
    scroll_mode_active = False 

    try:
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Checagem de Clique Direito (Polegar -> Anelar)
        right_click_dist = get_gesture_distance(hand_landmarks, 4, 16)
        
        if right_click_dist < config.CLICK_DISTANCE_THRESHOLD:
            if not dragging:
                print("🖱️ Right Click! (Polegar -> Anelar)")
                pyautogui.rightClick()
                time.sleep(0.3)
            return

        # Checagem de Clique Esquerdo
        left_click_dist = get_left_click_distance(hand_landmarks)
        is_clicking = left_click_dist < config.CLICK_DISTANCE_THRESHOLD
        is_intent_to_click = left_click_dist < config.CLICK_INTENT_THRESHOLD

        if dragging or (not is_intent_to_click):
            lm5, lm12, point_c, smoothed_point_c = calculate_vector(hand_landmarks)
            if lm5 and lm12 and point_c:
                
                cursor_color = (255, 0, 0) # Azul (Movendo)
                if dragging:
                    cursor_color = (0, 0, 255) # Vermelho (Arrastando)

                cv2.line(frame, lm5, lm12, (0, 255, 0), 2)
                cv2.line(frame, lm12, point_c, (0, 0, 255), 2)
                cv2.circle(frame, point_c, 7, cursor_color, -1)

                if smoothed_point_c:
                    cursor_x = int(smoothed_point_c[0] * config.SCREEN_WIDTH)
                    cursor_y = int(smoothed_point_c[1] * config.SCREEN_HEIGHT)
                    cursor_x = max(0, min(config.SCREEN_WIDTH - 1, cursor_x))
                    cursor_y = max(0, min(config.SCREEN_HEIGHT - 1, cursor_y))
                    
                    pyautogui.moveTo(cursor_x, cursor_y)
                    
                    if dragging:
                         print(f"🖱️ Arrastando cursor para: {cursor_x}, {cursor_y}")
        else:
            frozen_x = int(previous_point_c[0] * 640)
            frozen_y = int(previous_point_c[1] * 480)
            cv2.circle(frame, (frozen_x, frozen_y), 7, (0, 255, 255), -1) # Amarelo
            print("❄️ Cursor Congelado (Pronto para clicar)")

        # Processar o clique esquerdo (mouseDown / mouseUp)
        if is_clicking:
            if not dragging:
                pyautogui.mouseDown()
                dragging = True
                print("🖱️ Mouse Click & Hold (Drag Iniciado)")
        else:
            if dragging:
                pyautogui.mouseUp()
                dragging = False
                print("🖱️ Mouse Solto")

    except Exception as e:
        print(f"⚠️ Erro em handle_pointing: {e}")