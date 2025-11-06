import cv2
import config  # Importa seu config.py

# --- Importação dos Módulos de Hardware e Lógica ---
try:
    # 1. Módulo de Banco de Dados
    import db
    print("✅ Módulo 'db.py' importado.")
except ConnectionError as e:
    # Este erro é o 'raise' que colocamos no db.py
    print(f"❌ Erro fatal de conexão com o banco: {e}")
    print("Verifique suas chaves no .env e a conexão com o Supabase.")
    exit()

try:
    # 2. Módulo de Visão
    import vision
    print("✅ Módulo 'vision.py' importado e modelo de IA carregado.")
except ConnectionError as e:
    # Este erro é o 'raise' do vision.py
    print(f"❌ Erro fatal: {e}")
    print("Verifique o caminho do modelo em config.py.")
    exit()

# 3. Módulo da Balança
import balanca_leitura as balanca
print("✅ Módulo 'balanca_leitura.py' importado.")


# --- FASE 1: INICIALIZAÇÃO (SETUP) ---
print("\n" + "="*50)
print("--- INICIANDO SISTEMA DE CHECKOUT AUTOMÁTICO ---")
print("="*50)

# 1. Carregar produtos do Supabase para o cache local
print("Conectando ao banco de dados para carregar produtos...")
produtos_locais_cache = db.carregar_produtos()
if not produtos_locais_cache:
    print("❌ Erro fatal: Nenhum produto foi carregado do banco. Encerrando.")
    exit()

# 2. Conectar à Balança
# (Altere 'COM6' para a porta serial correta do seu Arduino)
balanca_serial = balanca.conectar_balanca(port='COM4') 
if balanca_serial is None:
    print("❌ Erro fatal: Não foi possível conectar à balança. Encerrando.")
    exit()

# 3. Inicializar a Câmera
print("Inicializando a webcam...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Erro fatal: Não foi possível abrir a webcam.")
    balanca_serial.close()
    exit()

print("\n" + "="*50)
print("✅ Sistema pronto. Aguarde o cliente...")
print("="*50)

# --- FASE 2: LOOP DE TRANSAÇÕES ---
try:
    while True:
        
        # --- ETAPA 1: AGUARDAR O ITEM (BLOQUEANTE) ---
        # O programa para aqui e espera o usuário colocar um item
        peso_g = balanca.esperar_por_peso(balanca_serial)
        
        if peso_g <= 0: # (Pode acontecer se o usuário der Ctrl+C)
            break
            
        print(f"\n--- NOVA TRANSAÇÃO INICIADA ---")
        print(f"Peso detectado: {peso_g:.2f} g. Acionando câmera...")

        # --- ETAPA 2: CAPTURAR E IDENTIFICAR O PRODUTO ---
        # O programa para aqui por alguns segundos para analisar
        nome_produto, frame_analisado = vision.get_detections(cap, num_frames=20)

        # --- ETAPA 3: LÓGICA DE NEGÓCIO E CONFIRMAÇÃO ---
        
        if nome_produto:
            print(f"Produto Reconhecido: {nome_produto}")
            
            # Busca o produto no nosso cache local
            info_produto = produtos_locais_cache.get(nome_produto)
            
            if info_produto:
                # --- SUCESSO: PRODUTO ENCONTRADO E CADASTRADO ---
                
                # 1. Calcular tudo
                peso_kg = peso_g / 1000.0
                preco_total = peso_kg * info_produto['preco']
                
                # 2. MOSTRAR A MENSAGEM DE CONFIRMAÇÃO (Sua nova ideia)
                print("\n" + "-"*30)
                print(f"Você quer comprar {peso_kg:.3f} kg de {nome_produto}?")
                print(f"Preço Final: R$ {preco_total:.2f}")
                print("-" * 30)

                # 3. Pedir a confirmação do usuário (BLOQUEANTE)
                confirmacao = input("Confirmar compra? (s/n): ").lower().strip()
                
                if confirmacao == 's':
                    # 4. ATUALIZAR O ESTOQUE NO BANCO DE DADOS
                    sucesso, msg = db.atualizar_estoque(nome_produto, peso_kg, produtos_locais_cache)
                    print(f"  Resultado da Compra: {msg}")
                else:
                    print("  Compra cancelada pelo usuário.")
                
            else:
                # Produto detectado, mas não está no nosso cache
                print(f"⚠️ ERRO: Produto '{nome_produto}' foi detectado, mas não está cadastrado no banco.")
        
        else:
            # IA não conseguiu identificar o produto
            print("❌ ERRO: Nenhum produto foi reconhecido com confiança. Por favor, reposicione o item.")

        # --- ETAPA 4: AGUARDAR REMOÇÃO (BLOQUEANTE) ---
        
        # Mostra o frame que foi analisado (para o operador ver o que a IA viu)
        cv2.imshow("Última Detecção", frame_analisado)
        print("\n(Pressione qualquer tecla na janela da imagem para fechar e continuar...)")
        cv2.waitKey(0) # Espera uma tecla na janela do OpenCV
        cv2.destroyAllWindows() #destroi todas as janelas do OpenCV
        
        # Agora, bloqueia até o peso ser removido
        balanca.esperar_zerar(balanca_serial)
        print("\n" + "="*50)
        print("✅ Balança zerada. Pronto para o próximo item...")
        print("="*50)

except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário.")

finally:
    # --- FASE 3: FINALIZAÇÃO (LIMPEZA) ---
    print("Encerrando conexões...")
    if 'balanca_serial' in locals() and balanca_serial.is_open:
        balanca_serial.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Aplicação encerrada.")