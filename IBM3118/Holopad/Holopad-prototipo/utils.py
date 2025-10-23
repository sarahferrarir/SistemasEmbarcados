# Guarda funções auxiliares para detecção de gestos e cálculos.

import numpy as np
from config import FINGER_DISTANCE_THRESHOLD, SCROLL_FINGER_THRESHOLD

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

        is_closed = (index_tip.y > index_pip.y and
                     middle_tip.y > middle_pip.y and
                     ring_tip.y > ring_pip.y and
                     pinky_tip.y > pinky_pip.y)
        
        return is_closed
    except Exception as e:
        print(f"⚠️ Erro em is_fist: {e}")
        return False