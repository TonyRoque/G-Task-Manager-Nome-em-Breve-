import json
import os
from datetime import datetime, date

# --- CONFIGURAÇÕES DO SISTEMA ---
ARQUIVO_SAVE = "save_player.json"
DANO_POR_QUEST_FALHA = 10  # Valor fixo de punição na V0.2

# --- FUNÇÕES DE PERSISTÊNCIA ---

def salvar_dados(dados):
    """Salva os dados, convertendo objetos de data em strings para o JSON."""
    # Fazemos uma cópia para não alterar o objeto original em uso
    dados_para_salvar = dados.copy()
    if isinstance(dados_para_salvar.get("ultimo_acesso"), (date, datetime)):
        dados_para_salvar["ultimo_acesso"] = dados_para_salvar["ultimo_acesso"].isoformat()
    
    with open(ARQUIVO_SAVE, "w") as arquivo:
        json.dump(dados_para_salvar, arquivo, indent=4)

def carregar_dados():
    """Carrega os dados e converte a string de data de volta para objeto date."""
    if os.path.exists(ARQUIVO_SAVE):
        with open(ARQUIVO_SAVE, "r") as arquivo:
            dados = json.load(arquivo)
            # Converte a string ISO de volta para objeto date
            if dados.get("ultimo_acesso"):
                dados["ultimo_acesso"] = date.fromisoformat(dados["ultimo_acesso"])
            return dados
    return None

# --- LÓGICA DO VIGILANTE (TEMPO) ---

def verificar_passagem_tempo(player):
    """
    Compara a data atual com o último acesso.
    Se houver virada de dia, pune por quests pendentes.
    """
    hoje = date.today()
    ultimo_acesso = player.get("ultimo_acesso")

    if ultimo_acesso and hoje > ultimo_acesso:
        print(f"\n[SISTEMA] Verificando progresso desde {ultimo_acesso}...")
        
        # Conta quantas quests não foram concluídas
        pendentes = [q for q in player["quests"] if q["status"] == "Pendente"]
        
        if pendentes:
            total_dano = len(pendentes) * DANO_POR_QUEST_FALHA
            player["hp"] -= total_dano
            print(f"[AVISO] Você deixou {len(pendentes)} quests incompletas.")
            print(f"[PUNIÇÃO] Você recebeu {total_dano} de dano no HP.")
        else:
            print("[SISTEMA] Todas as metas anteriores foram batidas. HP conservado.")

        # Limpa as quests do dia anterior para o novo ciclo (Opcional: pode-se deletar ou marcar como falhas)
        player["quests"] = [] 
        print("[SISTEMA] Quadro de missões resetado para o novo dia.")

    # Atualiza o carimbo de data para hoje
    player["ultimo_acesso"] = hoje
    salvar_dados(player)

# --- FUNÇÕES DE PERSONAGEM ---

def criar_personagem():
    print("\n" + "="*40)
    print("      [SISTEMA: CONTRATO DE DESPERTAR]      ")
    print("="*40)
    nome = input("Informe seu nome para o registro: ")
    
    novo_player = {
        "nome": nome,
        "nivel": 1,
        "xp": 0,
        "xp_proximo_nivel": 100,
        "hp": 100,
        "ultimo_acesso": date.today(),
        "quests": []
    }
    salvar_dados(novo_player)
    return novo_player

def verificar_permadeath(player):
    if player["hp"] <= 0:
        print("\n" + "!"*40)
        print("         VOCÊ MORREU. GAME OVER.         ")
        print("!"*40)
        if os.path.exists(ARQUIVO_SAVE):
            os.remove(ARQUIVO_SAVE)
        exit()

# --- FUNÇÕES DE QUESTS ---

def adicionar_quest(player):
    print("\n--- [NOVA QUEST DETECTADA] ---")
    descricao = input("O que deve ser feito? ")
    print("Dificuldades: 1. Fácil (+10xp) | 2. Média (+30xp) | 3. Difícil (+80xp)")
    opcao = input("Escolha: ")
    
    dificuldades = {"1": "Fácil", "2": "Média", "3": "Difícil"}
    dif = dificuldades.get(opcao, "Fácil")

    player["quests"].append({"tarefa": descricao, "dificuldade": dif, "status": "Pendente"})
    salvar_dados(player)

def listar_quests(player):
    if not player["quests"]:
        print("\n[!] Nenhuma quest ativa.")
        return

    print("\n--- [LISTA DE QUESTS ATIVAS] ---")
    for i, q in enumerate(player["quests"]):
        print(f"{i + 1}. [{q['status']}] {q['tarefa']} ({q['dificuldade']})")
    
    escolha = input("\nNúmero para concluir (ou 0 para voltar): ")
    if escolha.isdigit() and int(escolha) > 0:
        concluir_quest(player, int(escolha) - 1)

def concluir_quest(player, index):
    if index >= len(player["quests"]): return
    
    quest = player["quests"][index]
    if quest["status"] == "Concluída": return

    recompensas = {"Fácil": 10, "Média": 30, "Difícil": 80}
    player["xp"] += recompensas.get(quest["dificuldade"], 10)
    quest["status"] = "Concluída"
    
    if player["xp"] >= player["xp_proximo_nivel"]:
        player["nivel"] += 1
        player["xp"] -= player["xp_proximo_nivel"]
        print(f"\n[SISTEMA] LEVEL UP! Nível atual: {player['nivel']}")
    
    salvar_dados(player)

# --- MOTOR PRINCIPAL ---

def main():
    player = carregar_dados()
    if not player:
        player = criar_personagem()
    
    # Aciona o Vigilante logo no login
    verificar_passagem_tempo(player)
    
    while True:
        verificar_permadeath(player)
        print(f"\n>> {player['nome']} | LVL: {player['nivel']} | HP: {player['hp']}/100 | XP: {player['xp']}/{player['xp_proximo_nivel']} <<")
        print("1. Ver/Concluir Quests")
        print("2. Adicionar Quest")
        print("3. Sair")
        
        op = input("Ação: ")
        if op == "1": listar_quests(player)
        elif op == "2": adicionar_quest(player)
        elif op == "3": break

if __name__ == "__main__":
    main()