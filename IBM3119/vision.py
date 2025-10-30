import cv2
from ultralytics import YOLO
import config
from collections import Counter

# CARREGAR MODELO
try:

    model = YOLO(config.MODELO_PATH)
    print(f"✅ Modelo {config.MODELO_PATH} carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar o modelo: {e}")
    raise ConnectionError("❌ Falha ao carregar o modelo de IA") from e

def get_detections(cap: cv2.VideoCapture, num_frames: int = 10):
    """
    Captura 'N' frames da webcam, analisa todos e retorna a detecção 
    mais comum e estável encontrada.

    Args:
        cap: O objeto cv2.VideoCapture (sua webcam).
        num_frames: O número de frames para analisar. (Docstring corrigido)

    Returns:
        (str | None): O nome da classe mais detectada (ex: 'apple'), ou None se nada for encontrado.
        (cv2.Mat): O último frame capturado, para que o main.py possa exibi-lo.
    """

    print(f"🔃Analisando {num_frames} frames para estabilizar...")
    detections_list = [] #armazenar as detecoes 
    last_frame = None

    # --- INÍCIO DO LOOP DE CAPTURA DE FRAMES ---
    for i in range(num_frames):
        ret, frame = cap.read() #captura frame
        if not ret:
            print("Erro ao capturar frame da webcam.")
            continue

        last_frame = frame #guarda frame mais recente para exibir

        results = model(frame, verbose=False) #modelo faz detecao no frame

        best_detection = None #armazenar melhor detecao do frame
        max_confidence = config.CONFIDENCE_THRESHOLD #limiar de confianca

        # ENCONTRAR A MELHOR DETECAO NESSE FRAME
        for result in results:
            for box in result.boxes:
                confidence = box.conf[0].item()

                if confidence >= max_confidence:
                    max_confidence = confidence
                    best_detection = result.names[int(box.cls[0].item())]

        # Adiciona o "voto" deste frame à lista
        if best_detection:
            detections_list.append(best_detection)
            
    # --- FIM DO LOOP DE CAPTURA DE FRAMES ---

    
    # --- CONTAGEM DE VOTOS PARA RETORNAR O PRODUTO MAIS CONFIAVEL ---
    if not detections_list:
        print("❌ Nenhuma detecção confiável encontrada nos frames.")
        return None, last_frame # Retorna "Nenhum" e o último frame
    
    try:
        #usar counter para econtrar a detecao mais comum
        counter = Counter(detections_list)
        most_common_product, count = counter.most_common(1)[0]

        # (Correção no cálculo para ser mais preciso)
        stability = (count / len(detections_list)) * 100
        print(f"✅ Detecção estável: {most_common_product} (encontrado em {stability:.0f}% dos frames válidos)")
        return most_common_product, last_frame #retorna o produto mais comum e o frame
    
    except Exception as e:
        print(f"❌ Erro ao determinar a detecção mais comum: {e}")
        return None, last_frame