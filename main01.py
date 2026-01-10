import json
import os

# --- CONFIGURAÇÕES DO SISTEMA ---
ARQUIVO_SAVE = "save_player.json"

# --- FUNÇÕES DE PERSISTÊNCIA (SAVE/LOAD) ---

def salvar_dados(dados):
    """Grava as informações do jogador no arquivo JSON no Linux."""
    with open(ARQUIVO_SAVE, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)

def carregar_dados():
    """Tenta carregar o progresso. Se não existir, retorna None."""
    if os.path.exists(ARQUIVO_SAVE):
        with open(ARQUIVO_SAVE, "r") as arquivo:
            return json.load(arquivo)
    return None

# --- FUNÇÕES DE PERSONAGEM ---

def criar_personagem():
    """Inicia o Contrato do Despertar (Cadastro inicial)."""
    print("\n" + "="*40)
    print("      [SISTEMA: CONTRATO DE DESPERTAR]      ")
    print("="*40)
    nome = input("Informe seu nome para o registro: ")
    
    # Atributos iniciais do Jogador (V0.1)
    novo_player = {
        "nome": nome,
        "nivel": 0,
        "xp": 0,
        "xp_proximo_nivel": 100,
        "hp": 100,
        "quests": []  # Nossa 'mochila' de tarefas
    }
    
    salvar_dados(novo_player)
    print(f"\n[SISTEMA] Registro concluído. Boa sorte, Caçador {nome}.")
    return novo_player

def verificar_permadeath(player):
    """Se o HP chegar a 0, deleta o save e encerra o programa."""
    if player["hp"] <= 0:
        print("\n" + "!"*40)
        print("         VOCÊ MORREU. GAME OVER.         ")
        print("   O REGISTRO DO CAÇADOR FOI DELETADO.   ")
        print("!"*40)
        
        if os.path.exists(ARQUIVO_SAVE):
            os.remove(ARQUIVO_SAVE)
        exit()

# --- FUNÇÕES DE QUESTS (TAREFAS) ---

def adicionar_quest(player):
    """Adiciona uma nova tarefa com dificuldade definida."""
    print("\n--- [NOVA QUEST DETECTADA] ---")
    descricao = input("O que deve ser feito? ")
    print("Dificuldades: 1. Fácil | 2. Média | 3. Difícil")
    opcao = input("Escolha (1/2/3): ")
    
    dificuldades = {"1": "Fácil", "2": "Média", "3": "Difícil"}
    dif = dificuldades.get(opcao, "Fácil")

    nova_quest = {
        "tarefa": descricao,
        "dificuldade": dif,
        "status": "Pendente"
    }

    player["quests"].append(nova_quest)
    salvar_dados(player)
    print(f"[SISTEMA] Quest '{descricao}' registrada.")

def listar_quests(player):
    """Mostra as tarefas e permite concluir uma."""
    if not player["quests"]:
        print("\n[!] Nenhuma quest ativa no momento.")
        return

    print("\n--- [LISTA DE QUESTS ATIVAS] ---")
    for i, q in enumerate(player["quests"]):
        print(f"{i + 1}. [{q['status']}] {q['tarefa']} ({q['dificuldade']})")
    
    print("\n0. Voltar")
    escolha = input("Digite o número para concluir (ou 0): ")
    
    if escolha.isdigit():
        idx = int(escolha) - 1
        if 0 <= idx < len(player["quests"]):
            concluir_quest(player, idx)

def concluir_quest(player, index):
    """Aplica recompensas de XP ao completar uma tarefa."""
    quest = player["quests"][index]
    
    if quest["status"] == "Concluída":
        print("[!] Esta quest já foi finalizada.")
        return

    # Valores de recompensa
    recompensas = {"Fácil": 10, "Média": 30, "Difícil": 80}
    ganho_xp = recompensas.get(quest["dificuldade"], 10)

    quest["status"] = "Concluída"
    player["xp"] += ganho_xp
    
    print(f"\n[SISTEMA] +{ganho_xp} XP adquirido!")
    
    # Lógica de Level Up
    if player["xp"] >= player["xp_proximo_nivel"]:
        player["nivel"] += 1
        player["xp"] -= player["xp_proximo_nivel"] # Mantém o que sobrou de XP
        print(f"\n>>> LEVEL UP! VOCÊ AGORA É NÍVEL {player['nivel']} <<<")
    
    salvar_dados(player)

# --- MOTOR PRINCIPAL ---

def main():
    player = carregar_dados()

    if not player:
        player = criar_personagem()
    
    while True:
        verificar_permadeath(player)
        
        # Dashboard Principal
        print("\n" + "="*45)
        print(f" CAÇADOR: {player['nome']} | LVL: {player['nivel']}")
        print(f" HP: {player['hp']}/100 | XP: {player['xp']}/{player['xp_proximo_nivel']}")
        print("="*45)
        print("1. Ver/Concluir Quests")
        print("2. Adicionar Nova Quest")
        print("3. Sair")
        
        opcao = input("\nO que deseja fazer? ")
        
        if opcao == "1":
            listar_quests(player)
        elif opcao == "2":
            adicionar_quest(player)
        elif opcao == "3":
            print("\nSincronizando dados com o Sistema... Até logo.")
            break
        else:
            print("[!] Comando inválido.")

if __name__ == "__main__":
    main()
