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
    print("Banco de dados carregado com sucesso!")
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

    for box in results[0].boxes:

        # Pegar o nome da fruta
        class_id = int(box.cls[0])
        object_name = results[0].names[class_id]

        try:
            # Consulta a tabela para encontrar o objeto (fruta) pelo nome 
            response = supabase.table("frutas").select("produto_nome","preco_kg").eq("produto_nome", object_name).execute()

            # Caso a consulta seja aconteça com sucesso, vai imprimir o nome (produto_nome) e o preço por kilo da fruta (preco)
            if response.data:
                produto_info = response.data[0]
                nome = produto_info.get("produto_nome")
                preco = produto_info.get("preco_kg")

            # Pega as coordenadas da caixa onde o sistema detecto a fruta
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Texto de saida dos dados da fruta
            info = f"Nome da fruta: {nome} | Preço: {preco}/kg"

            # Configurações para a saida dos dados
            cv2.putText(annotated_frame, info, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        except Exception as e:
            print(f"Erro ao detectar a fruta: {e}")

    # Exibe o frame com as detecções em uma janela
    cv2.imshow("Detecção de Objetos YOLOv8", annotated_frame)

    # Encerra detecção caso apertar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos ao finalizar
cap.release()
cv2.destroyAllWindows()
print("Aplicação encerrada.")
