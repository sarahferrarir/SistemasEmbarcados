# Melhora a versão inicial: menos lag no cursor, e melhor precisão para o click.
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
# import pygetwindow as gw  # Removido para performance

# Parâmetros Ajustáveis
FINGER_DISTANCE_THRESHOLD = 0.05  # Distância para "juntar" os dedos
VECTOR_MULTIPLIER = 4.0 # Controls how far point C extends
SENSITIVITY = 0.5  # Suavização (0.1 - 1.0) Adjusts how quickly point C moves
DEADZONE = 0.04 # Ignores small movements (prevents jitter)
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# --- NOVAS CONSTANTES ---
# Distância exata para o clique ser registrado
CLICK_DISTANCE_THRESHOLD = 0.05 
# Distância para "congelar" o cursor. Deve ser MAIOR que o CLICK_DISTANCE_THRESHOLD
CLICK_INTENT_THRESHOLD = 0.08   


# --- Variáveis de Estado ---
dragging = False
previous_point_c = (0.5, 0.5)  # Iniciar no centro

def get_click_distance(hand_landmarks):
    """Retorna a distância entre o Polegar (4) e o PIP do Indicador (6)."""
    try:
        thumb_tip = hand_landmarks.landmark[4]
        index_pip = hand_landmarks.landmark[6]

        # Calculate Euclidean distance
        distance = np.hypot(thumb_tip.x - index_pip.x, thumb_tip.y - index_pip.y)
        # print(f"DEBUG: Distância Clique = {distance:.4f}")

        return distance
    except Exception as e:
        print(f"⚠️ Erro em get_click_distance: {e}")
        return 1.0  # Retorna distância grande em caso de erro

def calculate_vector(hand_landmarks):
    """Calcula o vetor 5 -> 12 -> C, aplicando suavização e deadzone."""
    global previous_point_c
    try:
        lm5 = hand_landmarks.landmark[5]
        lm12 = hand_landmarks.landmark[12]

        # Compute direction and extend for point C
        direction_x = lm12.x - lm5.x
        direction_y = lm12.y - lm5.y
        point_c_x = lm5.x + VECTOR_MULTIPLIER * direction_x
        point_c_y = lm5.y + VECTOR_MULTIPLIER * direction_y

        # Calculate movement difference from last frame
        delta_x = abs(point_c_x - previous_point_c[0])
        delta_y = abs(point_c_y - previous_point_c[1])

        # Apply deadzone (ignore small movements)
        if delta_x < DEADZONE and delta_y < DEADZONE:
            point_c_x, point_c_y = previous_point_c  # Keep the previous position

        # Apply sensitivity (scales movement)
        smoothed_x = previous_point_c[0] + (point_c_x - previous_point_c[0]) * SENSITIVITY
        smoothed_y = previous_point_c[1] + (point_c_y - previous_point_c[1]) * SENSITIVITY

        # Store new position for the next frame
        previous_point_c = (smoothed_x, smoothed_y)

        # Convert to pixel coordinates
        lm5_px = (int(lm5.x * 640), int(lm5.y * 480))
        lm12_px = (int(lm12.x * 640), int(lm12.y * 480))
        point_c_px = (int(smoothed_x * 640), int(smoothed_y * 480))

        # print(f"🖱️ Point C (Pixels): {point_c_px}")
        return lm5_px, lm12_px, point_c_px, (smoothed_x, smoothed_y)
    except Exception as e:
        print(f"⚠️ Erro em calculate_vector: {e}")
        return None, None, None, None

def fingers_together(hand_landmarks):
    """Verifica se os dedos indicador e médio estão juntos."""
    try:
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        distance = np.hypot(index_tip.x - middle_tip.x, index_tip.y - middle_tip.y)

        return distance < FINGER_DISTANCE_THRESHOLD # Uses the adjustable threshold

    except Exception as e:
        print(f"⚠️ Erro em fingers_together: {e}")
        return False

def process_hand(frame, hand_landmarks):
    """Função principal que gerencia todos os estados, desenho e controle do mouse."""
    global dragging
    
    try:
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # 1. Modo de "Apontar": Só move o cursor se os dedos estiverem juntos
        if not fingers_together(hand_landmarks):
            print("✋ Cursor desativado - Dedos separados")
            if dragging:  # Se estava arrastando, solte
                pyautogui.mouseUp()
                dragging = False
                print("🖱️ Mouse Solto (Dedos separados)")
            return  # Não faz mais nada

        # 2. Modo "Apontar" está ATIVO. Verifique o estado do clique.
        click_distance = get_click_distance(hand_landmarks)

        # 3. Lógica de Estado: Mover, Congelar ou Clicar?
        is_clicking = click_distance < CLICK_DISTANCE_THRESHOLD
        is_intent_to_click = click_distance < CLICK_INTENT_THRESHOLD # Zona de "congelamento"

        # O cursor se move se:
        # 1. O usuário está apenas apontando (sem intenção de clique)
        # 2. O usuário já está no modo "arrastar" (dragging)
        if dragging or (not is_intent_to_click):
            lm5, lm12, point_c, smoothed_point_c = calculate_vector(hand_landmarks)
            if lm5 and lm12 and point_c:
                cv2.line(frame, lm5, lm12, (0, 255, 0), 2)
                cv2.line(frame, lm12, point_c, (0, 0, 255), 2)
                cv2.circle(frame, point_c, 5, (255, 0, 0), -1)

                # Mover o cursor (RÁPIDO, sem 'duration')
                if smoothed_point_c:
                    cursor_x = int(smoothed_point_c[0] * SCREEN_WIDTH)
                    cursor_y = int(smoothed_point_c[1] * SCREEN_HEIGHT)
                    cursor_x = max(0, min(SCREEN_WIDTH - 1, cursor_x))
                    cursor_y = max(0, min(SCREEN_HEIGHT - 1, cursor_y))
                    
                    pyautogui.moveTo(cursor_x, cursor_y) # ✅ CORREÇÃO DE PERFORMANCE
                    
                    if dragging:
                         print(f"🖱️ Arrastando cursor para: {cursor_x}, {cursor_y}")
                    # else:
                        # print(f"🖱️ Movendo cursor para: {cursor_x}, {cursor_y}") # Spam
        else:
            # Isso agora só acontece no momento EXATO antes do clique
            print("❄️ Cursor Congelado (Pronto para clicar)")

        # 4. Processar o clique (mouseDown / mouseUp)
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
        print(f"⚠️ Erro em process_hand: {e}")

# --- Inicialização ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# --- Loop Principal ---
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Câmera não detectada!")
        break

    frame = cv2.flip(frame, 1)
    
    # Processa a imagem
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        # A nova função process_hand gerencia tudo
        process_hand(frame, results.multi_hand_landmarks[0])

    cv2.imshow('Holopad Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()