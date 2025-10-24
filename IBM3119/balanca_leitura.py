import serial
import time

# --- CONSTANTES ---
PESO_MINIMO_G = 20.0  # Peso mínimo para considerar que um item foi colocado 
PESO_ZERADO_G = 10.0  # Peso máximo para considerar que a balança está "zerada" 


def conectar_balanca(port='COM3', baudrate=57600) -> serial.Serial | None:
    """
    Tenta se conectar à porta serial especificada.
    Retorna o objeto 'serial' em caso de sucesso, ou None em caso de falha.
    """
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
    
        time.sleep(2) 
        ser.flushInput() # Limpa qualquer lixo inicial da porta serial
        print(f"✅ Conexão com a balança na porta {port} bem-sucedida.")
        return ser
    except serial.SerialException as e:
        print(f"❌ ERRO: Não foi possível conectar na balança ({port}): {e}")
        return None

def esperar_por_peso(ser: serial.Serial) -> float:
    """
    "função com loop de leitura" (BLOQUEANTE).
    Ela monitora a balança e só retorna quando um peso estável
    acima do limiar é detectado.
    
    Retorna:
        float: O peso estável detectado (em gramas).
    """
    print(f"\n--- ESTADO: AGUARDANDO ITEM (limiar > {PESO_MINIMO_G}g) ---")
    
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue

            peso = float(line)
            
            # O loop só continua se o peso for detectado
            if peso > PESO_MINIMO_G:
                print(f"Peso detectado: {peso:.2f} g. Aguardando estabilização...")
                
                # Espera o peso estabilizar
                time.sleep(1.0) # Espera 1 segundo
                line = ser.readline().decode('utf-8').strip()
                peso_estavel = float(line)
                
                print(f"Peso estável: {peso_estavel:.2f} g. Processando...")
                return peso_estavel
                
        except (ValueError, UnicodeDecodeError):
            # Ignora linhas de dados corrompidas ou iniciais
            pass
        except KeyboardInterrupt:
            print("Detecção interrompida pelo usuário.")
            return 0.0

def esperar_zerar(ser: serial.Serial):
    """
    Função BLOQUEANTE que espera o usuário remover o item.
    Só retorna quando o peso ficar ABAIXO do limiar de zerado.
    """
    print(f"\n--- ESTADO: AGUARDANDO REMOÇÃO (limiar < {PESO_ZERADO_G}g) ---")
    
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue

            peso = float(line)
            
            # O loop só continua quando o peso for removido
            if peso < PESO_ZERADO_G:
                print("Balança zerada. Pronto para o próximo item.")
                time.sleep(1.0) # Pausa para evitar detecção dupla
                ser.flushInput() # Limpa a fila de dados
                return
                
        except (ValueError, UnicodeDecodeError):
            pass
        except KeyboardInterrupt:
            print("Detecção interrompida pelo usuário.")
            return

#--- BLOCO DE TESTES ---
import serial
import time

# --- CONSTANTES ---
PESO_MINIMO_G = 10.0  # (Recomendo aumentar para 20.0 para evitar ruído)
PESO_ZERADO_G = 5.0   # (Recomendo aumentar para 10.0)


def conectar_balanca(port='COM3', baudrate=57600) -> serial.Serial | None:
    """
    Tenta se conectar à porta serial especificada.
    Retorna o objeto 'serial' em caso de sucesso, ou None em caso de falha.
    """
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2) 
        ser.flushInput() # Limpa qualquer lixo inicial da porta serial
        print(f"✅ Conexão com a balança na porta {port} bem-sucedida.")
        return ser
    except serial.SerialException as e:
        print(f"❌ ERRO: Não foi possível conectar na balança ({port}): {e}")
        return None

# Em balanca_leitura.py

def esperar_por_peso(ser: serial.Serial) -> float:
    """
    (BLOQUEANTE) Monitora a balança e só retorna quando um peso estável
    acima do limiar é detectado.
    """
    print(f"\n--- ESTADO: AGUARDANDO ITEM (limiar > {PESO_MINIMO_G}g) ---")
    
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue

            peso = float(line) 
            
            # 1. Gatilho de detecção
            if peso > PESO_MINIMO_G:
                print(f"Peso inicial detectado: {peso:.2f} g. Aguardando estabilização...")
                
                # 2. Espera 2 segundos para o peso estabilizar
                time.sleep(2.0) 
                
                # 3. Joga fora TODOS os valores intermediários
                ser.flushInput() 
                
                
                # Entra em um loop interno para "caçar" a próxima leitura válida.
                # Isso vence a "race condition" com o Arduino.
                print("Buffer limpo. Caçando a leitura estável...")
                while True:
                    try:
                        line_estavel = ser.readline().decode('utf-8').strip()
                        if line_estavel: # Se conseguimos ler uma linha
                            peso_estavel = float(line_estavel)
                            print(f"Peso estável: {peso_estavel:.2f} g. Processando...")
                            return peso_estavel + 5 # SUCESSO: Saímos da função
                    
                    except (ValueError, UnicodeDecodeError):
                        # Ignora linhas corrompidas, continua no sub-loop
                        pass
                    except KeyboardInterrupt:
                        print("Detecção interrompida pelo usuário.")
                        return 0.0
                # --- FIM DA CORREÇÃO ---
                
        except (ValueError, UnicodeDecodeError):
            pass
        except KeyboardInterrupt:
            print("Detecção interrompida pelo usuário.")
            return 0.0
        
def esperar_zerar(ser: serial.Serial):
    """
    (BLOQUEANTE) Espera o usuário remover o item.
    """
    print(f"\n--- ESTADO: AGUARDANDO REMOÇÃO (limiar < {PESO_ZERADO_G}g) ---")
    
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue

            peso = float(line)  # Ajuste para evitar ruído
            
            if peso < PESO_ZERADO_G:
                print("Balança zerada. Pronto para o próximo item.")
                time.sleep(1.0) 
                ser.flushInput() 
                return
                
        except (ValueError, UnicodeDecodeError):
            pass
        except KeyboardInterrupt:
            print("Detecção interrompida pelo usuário.")
            return

# --- BLOCO DE TESTES (NOVO - EM LOOP) ---
# (Este bloco só roda ao executar `python balanca_leitura.py`)
if __name__ == "__main__":
    
    # 1. Defina a porta COM correta aqui
    PORTA_BALANCA = 'COM3' # (Lembre-se de verificar se esta é a porta correta neste PC)
    
    print(f"--- INICIANDO TESTE DE LEITURA EM LOOP NA PORTA {PORTA_BALANCA} ---")
    print("Coloque um item na balança para iniciar.")
    print("Pressione Ctrl+C para parar.")
    
    balanca_serial = None # Definido fora para o 'finally'
    
    try:
        # 2. Conecta à balança
        balanca_serial = conectar_balanca(port=PORTA_BALANCA)
        
        if balanca_serial:
            
            # --- INÍCIO DO LOOP PRINCIPAL DO TESTE ---
            while True: 
                
                # 3. Espera o peso (BLOQUEANTE)
                peso_lido = esperar_por_peso(balanca_serial)
                
                # Verifica se o usuário pressionou Ctrl+C durante a espera
                if peso_lido <= 0: 
                    print("\nSinal de interrupção recebido.")
                    break # Sai do loop while True
                
                # 4. Imprime o resultado final da pesagem
                print("\n" + "="*30)
                print(f"PESO FINAL DETECTADO: {peso_lido:.2f} g")
                print("="*30)
                
                # 5. Espera a balança ser limpa (BLOQUEANTE)
                esperar_zerar(balanca_serial)
                
                # 6. Sinaliza que está pronto para o próximo item
                print("\nBalança limpa. Aguardando próximo item...")
                print("-" * 40)
            # --- FIM DO LOOP PRINCIPAL DO TESTE ---
        
        else:
            print("Falha ao conectar. Verifique a porta COM e a conexão do Arduino.")
            
    except KeyboardInterrupt:
        # Captura o Ctrl+C caso seja pressionado fora das funções de espera
        print("\nPrograma interrompido pelo usuário.")
    
    finally:
        # 7. Fecha a conexão de forma limpa ao sair do loop ou em caso de erro
        if balanca_serial and balanca_serial.is_open:
            balanca_serial.close()
            print("Conexão serial fechada.")
            
    print("--- TESTE CONCLUÍDO ---")