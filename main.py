import json
import os

# Nome do arquivo que guardará seu progresso no Linux
ARQUIVO_SAVE = "save_player.json"

def salvar_dados(dados):
    with open(ARQUIVO_SAVE, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)

def carregar_dados():
    # Verifica se o arquivo de save existe na pasta
    if os.path.exists(ARQUIVO_SAVE):
        with open(ARQUIVO_SAVE, "r") as arquivo:
            return json.load(arquivo)
    return None

def criar_personagem():
    print("\n--- [SISTEMA: CONTRATO DE DESPERTAR] ---")
    nome = input("Informe seu nome para o registro: ")
    
    # Estrutura inicial do Player
    novo_player = {
        "nome": nome,
        "nivel": 0,
        "xp": 0,
        "hp": 100,
        "meta_diaria": 3  # Valor padrão inicial
    }
    
    salvar_dados(novo_player)
    print(f"\n[SISTEMA] Registro concluído, Caçador {nome}. Não falhe.")
    return novo_player

def verificar_permadeath(player):
    if player["hp"] <= 0:
        print("\n" + "!"*40)
        print("Sua força se esgotou. O sistema foi encerrado.")
        print("CADASTRO DELETADO.")
        print("!"*40)
        
        # Deleta o arquivo de save no Linux
        if os.path.exists(ARQUIVO_SAVE):
            os.remove(ARQUIVO_SAVE)
        exit() # Fecha o programa

def main():
    player = carregar_dados()

    # Se não existe player, inicia o cadastro
    if not player:
        player = criar_personagem()
    
    # Verifica se o player "morreu" antes de continuar
    verificar_permadeath(player)

    # Painel Principal
    print(f"\n>>> STATUS: {player['nome']} | LVL: {player['nivel']} | HP: {player['hp']} <<<")
    print("1. Ver Quests (Em breve)")
    print("2. Sair")

if __name__ == "__main__":
    main()
