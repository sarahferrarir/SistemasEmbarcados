from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions # <-- IMPORTAR ISSO
import httpx # <-- IMPORTAR ISSO
import config

# CONFIGURAÇÃO DO BANCO DE DADOS 
try:

    options = ClientOptions(
        httpx_client=httpx.Client(verify=False)
    )

    # cria cliente
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY, options=options)
    print("✅ Conexão com o Supabase bem-sucedida!")
    print(f"chave api lida: {config.SUPABASE_KEY}")
except Exception as e:
    print(f"❌ Erro ao conectar com o Supabase: {e}")
    raise ConnectionError("Falha ao iniciar cliente supabase") from e

def carregar_produtos()-> dict:
    """
    Carrega a lista de produtos no Supabase num dicionario local

    Retorna: (dict) -> ({
        nome_produto: {
            preco,
            qtd
        }
    })
    """
    
    print("Carregando lista de produtos do supabase...")
    
    try:
        #query
        response = supabase.table('products').select('name,preco_kg,qtd_kg').execute()
        
        #query bem sucedida
        if response.data:
            produtos = {
                item['name']: {
                    'preco':item['preco_kg'],
                    'qtd_kg':item['qtd_kg']
                } for item in response.data
            }
            print(f"✅ {len(produtos)} Produtos carregados com sucesso localmente!")
            
            return produtos
        else:
            print("⚠️ Nenhum produto encontrado no banco!")
            return {}
        
    except Exception as e:
        print(f"🚫 Erro ao carregar os produtos: {e}")
        return {}

#descontar do estoque a compra efetuado
def atualizar_estoque(nome_produto:str,qtd_comprada:float,lista_produtos:dict):
    """
    Atualiza o estoque de um produto localmente e no Supabase.
    (Versão de protótipo, sem tratamento de concorrência)

    Retorna: (bool, str) -> (sucesso, mensagem_de_status)
    """
    
    if nome_produto not in lista_produtos:
        mensagem = "Erro: produto não encontrado no cache local!"
        return(False, mensagem)
    
    #pega os dados no cache local
    dados_produto = lista_produtos[nome_produto]
    estoque_atual = dados_produto['qtd_kg']
    
    #verifica se compra é possível comparando quantidade no estoque 
    if estoque_atual < qtd_comprada:
        mensagem = f"Erro: Quantidade no estoque insuficiente. Restam {estoque_atual:.2f} Kg"
        return(False, mensagem) 
    
    #debita no estoque
    estoque_atual -= qtd_comprada
    
    #atualiza no subase novo estoque
    print(f"🔄 Atualizando estoque de '{nome_produto}' no Supabase...")
    
    try:
        #update
        supabase.table('products').update({'qtd_kg': estoque_atual}).eq('name', nome_produto).execute()
        
        #atualiza cache local caso supabase for atualizado corretamente
        lista_produtos[nome_produto]['qtd_kg'] = estoque_atual
        
        mensagem = f"Compra realizada! Novo estoque de {nome_produto}: {estoque_atual:.3f} Kg"
        print(f"✅ {mensagem}")
        return(True,mensagem)
    
    except Exception as e:
        mensagem = "Erro ao atualizar estoque no SUPABASE"
        print(f"🚫 {mensagem}")
        return(False,mensagem)
    
    
# --- TESTES ---
# cache_local = carregar_produtos()
# print(cache_local)




        
