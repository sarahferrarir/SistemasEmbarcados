import cv2
from ultralytics import YOLO
from supabase import create_client, Client
import config
import PySimpleGUI as sg


# CONFIGURAÇÃO DO BANCO DE DADOS 
#importar o arquivo db.py e importar suas funções


# CARREGAR MODELO
try:

    model = YOLO(config.MODELO_PATH)
    print(f"✅ Modelo {config.MODELO_PATH} carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar o modelo: {e}")
    exit()

# Abre a webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro: Não foi possível abrir a webcam.")
    exit()

print("Webcam iniciada. Pressione 'q' para sair.")

# limiar de confiança 
CONFIDENCE_THRESHOLD = config.CONFIDENCE_THRESHOLD 

#Loop principal
while True:
    # Lê um frame da webcam
    ret, frame = cap.read()
    if not ret:
        print("Fim do stream de vídeo ou erro de captura.")
        break

    # Roda o modelo
    results = model(frame, verbose=False) 

    for result in results:
        
        for box in result.boxes:
            # Extrai o valor de confiança
            confidence = box.conf[0].item() 

            # --- filtragem ---
            
            # Só processa e desenha se a confiança for igual ou superior ao limiar
            if confidence >= CONFIDENCE_THRESHOLD:
                
                # coordenadas da caixa
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # nome da classe detectada
                name_class = result.names[int(box.cls[0].item())]

                # 3. Prepara o texto para exibição
                texto = f'{name_class} {confidence:.2f}'
                cor = (0, 255, 0) # Cor verde

                # 4. Desenha a caixa no frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
                
                # 5. Escreve o texto nome + confiança
                cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)

    # Exibe o frame final no OpenCV
    cv2.imshow("Detecção de Objetos", frame)

    # Verifica se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- FINALIZAÇÃO ---
print("Encerrando aplicação...")
cap.release()
cv2.destroyAllWindows()
print("Aplicação encerrada.")


