# Guarda todas as variáveis de configuração e constantes.

import pyautogui

# --- Parâmetros de Gestos ---
FINGER_DISTANCE_THRESHOLD = 0.05  # Distância para "juntar" os dedos (apontar)
SCROLL_FINGER_THRESHOLD = 0.07    # Distância para 3 dedos (scroll)

# --- Parâmetros de Clique ---
# Distância exata para o clique ser registrado (Left, Right)
CLICK_DISTANCE_THRESHOLD = 0.05
# Distância para "congelar" o cursor (deve ser MAIOR que o CLICK_DISTANCE_THRESHOLD)
CLICK_INTENT_THRESHOLD = 0.08   

# --- Parâmetros de Movimento ---
VECTOR_MULTIPLIER = 4.0           # Extensão do vetor de mira
SENSITIVITY = 0.5                 # Suavização de movimento (0.1 - 1.0)
DEADZONE = 0.04                   # Ignora pequenos movimentos (jitter)

# --- Parâmetros de Scroll ---
SCROLL_SENSITIVITY = 1            # Sensibilidade: quão rápido o scroll se move
SCROLL_DEADZONE = 0.02            # Zona Morta: impede "scroll fantasma"

# --- Configuração de Tela ---
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()