# deteccao_simples.py

# essa versão foi a primeira implementada: contém o modelo COCO do YOLOV8 que identifica objetos genéricos. Para o projeto final usaremos uma versão desse modelo com fine-tuning

import cv2
from ultralytics import YOLO
from supabase import create_client, Client
import config

# Teste de implementação com o banco de dados
try:
    url: str = config.SUPABASE_URL
    key: str = config.SUPABASE_API

    supabase: Client = create_client(url, key)
    print("Supabase carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o banco de dados: {e}")
    exit()

# --- CONFIGURAÇÃO DO MODELO ---

try:
    model = YOLO('modeloV1.pt')
    print("Modelo YOLOv8 carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    exit()


# Abre a webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro: Não foi possível abrir a webcam.")
    exit()

print("Webcam iniciada. Pressione 'q' para sair.")

while True:
    
    ret, frame = cap.read()
    if not ret:
        print("Fim do stream de vídeo ou erro de captura.")
        break

    
    results = model(frame, verbose=False) # verbose=False para não poluir o console

    # .plot() adiciona as detecções ao frame
    annotated_frame = results[0].plot()

    # Exibe o frame com as detecções em uma janela
    cv2.imshow("Detecção de Objetos YOLOv8", annotated_frame)

    # Encerra detecção caso apertar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos ao finalizar
cap.release()
cv2.destroyAllWindows()
print("Aplicação encerrada.")
