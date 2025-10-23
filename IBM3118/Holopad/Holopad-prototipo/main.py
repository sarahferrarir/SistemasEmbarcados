# Ponto de entrada principal do Holopad.
# Inicializa a câmera, MediaPipe e roda o loop principal de gestos.

import cv2
import mediapipe as mp
import pyautogui

# --- Importações dos Nossos Módulos ---
import cursor_control  # Para acessar os handlers (handle_pointing) e o estado (dragging)
from utils import (    # Para importar as funções de detecção de gestos
    is_scroll_gesture,
    fingers_together,
    is_hang_loose
)

# --- Orquestrador Principal ---

def process_gestures(frame, hand_landmarks, mp_draw, mp_hands):
    """
    Orquestrador. Decide qual gesto está ativo.
    Retorna 'False' se o gesto de 'Parar' for detectado.
    """
    # A ORDEM IMPORTA: Checa o gesto mais específico (3 dedos) primeiro.
    
    # 1. Gesto de Scroll (3 dedos)
    if is_scroll_gesture(hand_landmarks):
        if cursor_control.dragging:
            pyautogui.mouseUp()
            cursor_control.dragging = False
            print("🖱️ Mouse Solto (Mudou para Scroll)")
        
        cursor_control.handle_scrolling(frame, hand_landmarks)

    # 2. Gesto de Apontar (2 dedos)
    elif fingers_together(hand_landmarks):
        cursor_control.handle_pointing(frame, hand_landmarks, mp_draw, mp_hands)
    
    # 3. Modo Desativado (Dedos separados)
    else:
        # Reseta os estados
        cursor_control.scroll_mode_active = False
        if cursor_control.dragging:
            pyautogui.mouseUp()
            cursor_control.dragging = False
            print("🖱️ Mouse Solto (Dedos separados)")
            
        print("✋ Cursor desativado")
        
        # CHECAGEM DE "PARAR":
        if is_hang_loose(hand_landmarks):
            print("🛑 Gesto de PARAR (Hang Loose) detectado! Encerrando...")
            cv2.putText(frame, "PARANDO...", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            return False

    return True # Sinaliza para continuar rodando

# --- Função Principal de Execução ---

def main():
    """Inicializa e roda o aplicativo."""
    
    # Inicialização do MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils

    # Inicialização da Câmera
    cap = cv2.VideoCapture(0)
    
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
            # Passa mp_draw e mp_hands para os handlers poderem desenhar
            continue_running = process_gestures(frame, hand_landmarks, mp_draw, mp_hands)
        else:
            # Se a mão sair da tela, reseta os estados
            cursor_control.scroll_mode_active = False
            if cursor_control.dragging:
                pyautogui.mouseUp()
                cursor_control.dragging = False
                print("🖱️ Mouse Solto (Mão fora da tela)")

        cv2.imshow('Holopad Control', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- Limpeza Final ---
    print("Encerrando o programa.")
    cap.release()
    cv2.destroyAllWindows()

# --- Ponto de Entrada Padrão do Python ---
if __name__ == "__main__":
    main()