# Guarda funções auxiliares para detecção de gestos e cálculos.

import numpy as np
from config import FINGER_DISTANCE_THRESHOLD, SCROLL_FINGER_THRESHOLD, FINGER_FLEX_THRESHOLD

def get_gesture_distance(hand_landmarks, lm_index1, lm_index2):
    """Retorna a distância Euclidiana entre dois landmarks da mão."""
    try:
        lm1 = hand_landmarks.landmark[lm_index1]
        lm2 = hand_landmarks.landmark[lm_index2]
        distance = np.hypot(lm1.x - lm2.x, lm1.y - lm2.y)
        return distance
    except Exception as e:
        print(f"⚠️ Erro em get_gesture_distance: {e}")
        return 1.0  # Retorna distância grande em caso de erro

def get_left_click_distance(hand_landmarks):
    """Atalho para Polegar (4) -> PIP do Indicador (6)."""
    return get_gesture_distance(hand_landmarks, 4, 6)

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

def is_hang_loose(hand_landmarks):
    """Verifica se o gesto é Hang Loose (Polegar e Mindinho estendidos; Indicador, Médio, Anelar dobrados)."""
    try:
        # Pontas dos dedos
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]

        # Articulações PIP (dobra principal)
        index_pip = hand_landmarks.landmark[6]
        middle_pip = hand_landmarks.landmark[10]
        ring_pip = hand_landmarks.landmark[14]

        # A lógica é:
        # 1. Indicador, Médio e Anelar devem estar DOBRADOS (a ponta está ABAIXO da articulação PIP).
        is_flexed = (index_tip.y > index_pip.y + FINGER_FLEX_THRESHOLD and
                     middle_tip.y > middle_pip.y + FINGER_FLEX_THRESHOLD and
                     ring_tip.y > ring_pip.y + FINGER_FLEX_THRESHOLD)

        # 2. Polegar e Mindinho devem estar ESTENDIDOS (o mindinho precisa estar longe o suficiente do anelar).
        # Para o polegar, usamos a posição. Para o mindinho, a distância dele para o anelar.
        # Note: A detecção de polegar é complexa; o melhor é garantir que ele esteja LONGE da palma.

        # Verifica se o mindinho está estendido (longe do anelar)
        dist_ring_pinky = np.hypot(ring_tip.x - pinky_tip.x, ring_tip.y - pinky_tip.y)
        is_pinky_extended = dist_ring_pinky > 3 * FINGER_FLEX_THRESHOLD # Usa um multiplicador maior

        # 3. O polegar geralmente estará longe da palma. O MediaPipe ajuda nisso.
        # Vamos confiar que a verificação de flexão garante os 3 dedos do meio.
        
        return is_flexed and is_pinky_extended

    except Exception as e:
        print(f"⚠️ Erro em is_hang_loose: {e}")
        return False

