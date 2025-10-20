import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

#armazenamos em constantes Python
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# caminho do modelo
MODELO_PATH = "modeloV1.pt"

#confianca usada
CONFIDENCE_THRESHOLD = 0.70

# Verificação 
if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️  Atenção: Variáveis SUPABASE_URL ou SUPABASE_KEY não encontradas.")
    print("Certifique-se de ter um arquivo .env na raiz do projeto.")