# Adiciona novas funções: scroll, click com o botão esquerdo, parar e melhora a visibilidade.
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

# --- Parâmetros Ajustáveis ---
FINGER_DISTANCE_THRESHOLD = 0.05  # Distância para "juntar" os dedos (apontar)
VECTOR_MULTIPLIER = 4.0           # Extensão do vetor de mira
SENSITIVITY = 0.5                 # Suavização de movimento (0.1 - 1.0)
DEADZONE = 0.04                   # Ignora pequenos movimentos (jitter)
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# --- Constantes de Clique ---
# Distância exata para o clique ser registrado
CLICK_DISTANCE_THRESHOLD = 0.05
# Distância para "congelar" o cursor (deve ser MAIOR que o CLICK_DISTANCE_THRESHOLD)
CLICK_INTENT_THRESHOLD = 0.08   

# --- Constantes de Scroll (NOVO) ---
# Distância para considerar os 3 dedos de scroll juntos
SCROLL_FINGER_THRESHOLD = 0.07 
# Sensibilidade: quão rápido o scroll se move (use valores negativos para inverter)
SCROLL_SENSITIVITY = 1 
# Zona Morta: impede "scroll fantasma" por movimentos pequenos
SCROLL_DEADZONE = 0.02 

# --- Variáveis de Estado Globais ---
dragging = False
previous_point_c = (0.5, 0.5)  # Iniciar no centro
last_scroll_y = 0              # Guarda a posição Y anterior para o scroll
scroll_mode_active = False     # Controla a inicialização do modo scroll

# --- Funções Auxiliares (Helpers) ---

def get_gesture_distance(hand_landmarks, lm_index1, lm_index2):
    """(NOVA) Retorna a distância Euclidiana entre dois landmarks da mão."""
    try:
        lm1 = hand_landmarks.landmark[lm_index1]
        lm2 = hand_landmarks.landmark[lm_index2]
        distance = np.hypot(lm1.x - lm2.x, lm1.y - lm2.y)
        return distance
    except Exception as e:
        print(f"⚠️ Erro em get_gesture_distance: {e}")
        return 1.0  # Retorna distância grande em caso de erro

def get_left_click_distance(hand_landmarks):
    """(MODIFICADA) Atalho para Polegar (4) -> PIP do Indicador (6)."""
    return get_gesture_distance(hand_landmarks, 4, 6)

def calculate_vector(hand_landmarks):
    """Calcula o vetor 5 -> 12 -> C, aplicando suavização e deadzone."""
    global previous_point_c
    try:
        lm5 = hand_landmarks.landmark[5]
        lm12 = hand_landmarks.landmark[12]

        direction_x = lm12.x - lm5.x
        direction_y = lm12.y - lm5.y
        point_c_x = lm5.x + VECTOR_MULTIPLIER * direction_x
        point_c_y = lm5.y + VECTOR_MULTIPLIER * direction_y

        delta_x = abs(point_c_x - previous_point_c[0])
        delta_y = abs(point_c_y - previous_point_c[1])

        if delta_x < DEADZONE and delta_y < DEADZONE:
            point_c_x, point_c_y = previous_point_c

        smoothed_x = previous_point_c[0] + (point_c_x - previous_point_c[0]) * SENSITIVITY
        smoothed_y = previous_point_c[1] + (point_c_y - previous_point_c[1]) * SENSITIVITY

        previous_point_c = (smoothed_x, smoothed_y)

        lm5_px = (int(lm5.x * 640), int(lm5.y * 480))
        lm12_px = (int(lm12.x * 640), int(lm12.y * 480))
        point_c_px = (int(smoothed_x * 640), int(smoothed_y * 480))

        return lm5_px, lm12_px, point_c_px, (smoothed_x, smoothed_y)
    except Exception as e:
        print(f"⚠️ Erro em calculate_vector: {e}")
        return None, None, None, None

def fingers_together(hand_landmarks):
    """Verifica se os dedos indicador(8) e médio(12) estão juntos."""
    try:
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        distance = np.hypot(index_tip.x - middle_tip.x, index_tip.y - middle_tip.y)
        return distance < FINGER_DISTANCE_THRESHOLD
    except Exception as e:
        print(f"⚠️ Erro em fingers_together: {e}")
        return False

# --- NOVAS Funções de Gestos (Scroll e Punho) ---

def is_scroll_gesture(hand_landmarks):
    """Verifica se os dedos Indicador(8), Médio(12) e Anelar(16) estão juntos."""
    try:
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]

        dist_8_12 = np.hypot(index_tip.x - middle_tip.x, index_tip.y - middle_tip.y)
        dist_12_16 = np.hypot(middle_tip.x - ring_tip.x, middle_tip.y - ring_tip.y)

        return (dist_8_12 < SCROLL_FINGER_THRESHOLD) and (dist_12_16 < SCROLL_FINGER_THRESHOLD)
    
    except Exception as e:
        print(f"⚠️ Erro em is_scroll_gesture: {e}")
        return False

def is_fist(hand_landmarks):
    """Verifica se a mão está fechada (punho)."""
    try:
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]
        
        index_pip = hand_landmarks.landmark[6]
        middle_pip = hand_landmarks.landmark[10]
        ring_pip = hand_landmarks.landmark[14]
        pinky_pip = hand_landmarks.landmark[18]

        # Pontas dos dedos estão "abaixo" (Y maior) de suas articulações
        is_closed = (index_tip.y > index_pip.y and
                     middle_tip.y > middle_pip.y and
                     ring_tip.y > ring_pip.y and
                     pinky_tip.y > pinky_pip.y)
        
        return is_closed
    except Exception as e:
        print(f"⚠️ Erro em is_fist: {e}")
        return False
    
# --- Funções "Handler" (O que fazer com cada gesto) ---

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
    
    if abs(delta_y) > SCROLL_DEADZONE:
        scroll_amount = int(-delta_y * 100 * SCROLL_SENSITIVITY)
        if scroll_amount != 0:
            pyautogui.scroll(scroll_amount)
            print(f"📜 Scrolling: {scroll_amount}")

    last_scroll_y = current_y

def handle_pointing(frame, hand_landmarks):
    """Gerencia Apontar, Congelar, Clicar (L/R) e Arrastar."""
    global dragging, scroll_mode_active
    
    scroll_mode_active = False 

    try:
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # --- ✅ NOVO: CHECAGEM DE CLIQUE DIREITO ---
        # Polegar (4) tocando o Dedo ANELAR (16)
        right_click_dist = get_gesture_distance(hand_landmarks, 4, 16)
        
        if right_click_dist < CLICK_DISTANCE_THRESHOLD:
            if not dragging: # Evita clique direito durante um arraste
                print("🖱️ Right Click! (Polegar -> Anelar)")
                pyautogui.rightClick()
                time.sleep(0.3) # Cooldown para evitar cliques múltiplos
            return # Para a execução para não ativar o clique esquerdo
        # --- FIM DA CHECAGEM ---

        # Checagem de Clique Esquerdo (continua como antes)
        left_click_dist = get_left_click_distance(hand_landmarks)
        
        is_clicking = left_click_dist < CLICK_DISTANCE_THRESHOLD
        is_intent_to_click = left_click_dist < CLICK_INTENT_THRESHOLD

        # Move se (estiver arrastando) OU (não tiver intenção de clique)
        if dragging or (not is_intent_to_click):
            lm5, lm12, point_c, smoothed_point_c = calculate_vector(hand_landmarks)
            if lm5 and lm12 and point_c:
                
                # --- ✅ NOVO: LÓGICA DE COR (FEEDBACK VISUAL) ---
                cursor_color = (255, 0, 0) # Azul (Movendo)
                if dragging:
                    cursor_color = (0, 0, 255) # Vermelho (Arrastando)
                # --- FIM DA LÓGICA DE COR ---

                cv2.line(frame, lm5, lm12, (0, 255, 0), 2)
                cv2.line(frame, lm12, point_c, (0, 0, 255), 2)
                cv2.circle(frame, point_c, 7, cursor_color, -1) # Usa a cor dinâmica

                if smoothed_point_c:
                    cursor_x = int(smoothed_point_c[0] * SCREEN_WIDTH)
                    cursor_y = int(smoothed_point_c[1] * SCREEN_HEIGHT)
                    cursor_x = max(0, min(SCREEN_WIDTH - 1, cursor_x))
                    cursor_y = max(0, min(SCREEN_HEIGHT - 1, cursor_y))
                    
                    pyautogui.moveTo(cursor_x, cursor_y)
                    
                    if dragging:
                         print(f"🖱️ Arrastando cursor para: {cursor_x}, {cursor_y}")
        else:
            # --- ✅ NOVO: FEEDBACK VISUAL DE "CONGELADO" ---
            # Desenha um círculo amarelo onde o cursor parou
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

# --- Orquestrador Principal (Cérebro) ---

def process_gestures(frame, hand_landmarks):
    """
    Orquestrador. Decide qual gesto está ativo.
    Retorna 'False' se o gesto de 'Parar' for detectado.
    """
    global dragging, scroll_mode_active
    
    # A ORDEM IMPORTA: Checa o gesto mais específico (3 dedos) primeiro.
    
    # 1. Gesto de Scroll (3 dedos)
    if is_scroll_gesture(hand_landmarks):
        if dragging:
            pyautogui.mouseUp()
            dragging = False
            print("🖱️ Mouse Solto (Mudou para Scroll)")
        
        handle_scrolling(frame, hand_landmarks)

    # 2. Gesto de Apontar (2 dedos)
    elif fingers_together(hand_landmarks):
        handle_pointing(frame, hand_landmarks)
    
    # 3. Modo Desativado (Dedos separados)
    else:
        # Reseta os estados
        scroll_mode_active = False
        if dragging:
            pyautogui.mouseUp()
            dragging = False
            print("🖱️ Mouse Solto (Dedos separados)")
            
        print("✋ Cursor desativado")
        
        # CHECAGEM DE "PARAR":
        # Se os dedos estão separados E o usuário fechar a mão...
        if is_fist(hand_landmarks):
            print("🛑 Gesto de PARAR detectado! Encerrando...")
            cv2.putText(frame, "PARANDO...", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            return False # Sinaliza para o loop principal parar

    return True # Sinaliza para continuar rodando

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
continue_running = True
while continue_running: 
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Câmera não detectada!")
        break

    frame = cv2.flip(frame, 1)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        continue_running = process_gestures(frame, hand_landmarks)
    else:
        # Se a mão sair da tela, reseta os estados
        scroll_mode_active = False
        if dragging:
            pyautogui.mouseUp()
            dragging = False
            print("🖱️ Mouse Solto (Mão fora da tela)")


    cv2.imshow('Holopad Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Limpeza Final ---
print("Encerrando o programa.")
cap.release()
cv2.destroyAllWindows()