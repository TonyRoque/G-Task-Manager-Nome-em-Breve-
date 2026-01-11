import json
import os
from datetime import datetime, date

# --- CONFIGURAÇÕES E REQUISITOS ---
ARQUIVO_SAVE = "save_player.json"
DANO_POR_QUEST_FALHA = 10

# Definição dos Portões de Rank (Nível Mínimo e Total de Quests)
# Seguindo a lógica: Rank atual -> Requisitos para o PRÓXIMO
REQUISITOS_RANK = {
    "E": {"proximo": "D", "nivel": 15, "quests": 20},
    "D": {"proximo": "C", "nivel": 30, "quests": 50},
    "C": {"proximo": "B", "nivel": 50, "quests": 100},
    "B": {"proximo": "A", "nivel": 80, "quests": 250},
    "A": {"proximo": "S", "nivel": 100, "quests": 500},
    "S": {"proximo": None} # Rank Máximo
}

# --- FUNÇÕES DE PERSISTÊNCIA ---

def salvar_dados(dados):
    """Salva os dados garantindo que objetos de data sejam strings no JSON."""
    dados_para_salvar = dados.copy()
    if isinstance(dados_para_salvar.get("ultimo_acesso"), (date, datetime)):
        dados_para_salvar["ultimo_acesso"] = dados_para_salvar["ultimo_acesso"].isoformat()
    
    with open(ARQUIVO_SAVE, "w") as arquivo:
        json.dump(dados_para_salvar, arquivo, indent=4)

def carregar_dados():
    """Carrega o save e reconverte a string de data para objeto date."""
    if os.path.exists(ARQUIVO_SAVE):
        with open(ARQUIVO_SAVE, "r") as arquivo:
            dados = json.load(arquivo)
            if dados.get("ultimo_acesso"):
                dados["ultimo_acesso"] = date.fromisoformat(dados["ultimo_acesso"])
            return dados
    return None

# --- LÓGICA DE EVOLUÇÃO (RANK E LEVEL) ---

def verificar_ascensao_rank(player):
    """Verifica se o caçador atingiu os requisitos para subir de Rank."""
    rank_atual = player.get("rank", "E")
    regra = REQUISITOS_RANK.get(rank_atual)

    # Se não houver próximo rank ou regra não definida, encerra
    if not regra or not regra["proximo"]:
        return

    # Checa se atingiu AMBOS os requisitos (Nível E Quantidade de Quests)
    if player["nivel"] >= regra["nivel"] and player["total_concluido"] >= regra["quests"]:
        novo_rank = regra["proximo"]
        player["rank"] = novo_rank
        print(f"\n{'#'*45}")
        print(f"🎉 ASCENSÃO DETECTADA! VOCÊ AGORA É RANK [{novo_rank}] 🎉")
        print(f"{'#'*45}\n")
        salvar_dados(player)

# --- SISTEMA DE TAREFAS E TEMPO ---

def verificar_passagem_tempo(player):
    """Aplica punições se o dia virar com tarefas pendentes."""
    hoje = date.today()
    ultimo_acesso = player.get("ultimo_acesso")

    if ultimo_acesso and hoje > ultimo_acesso:
        print(f"\n[SISTEMA] Analisando ciclo anterior ({ultimo_acesso})...")
        pendentes = [q for q in player["quests"] if q["status"] == "Pendente"]
        
        if pendentes:
            total_dano = len(pendentes) * DANO_POR_QUEST_FALHA
            player["hp"] -= total_dano
            print(f"[PUNIÇÃO] {len(pendentes)} tarefas ignoradas. -{total_dano} HP.")
        
        player["quests"] = [] # Reset diário
        player["ultimo_acesso"] = hoje
        salvar_dados(player)

def concluir_quest(player, index):
    """Finaliza quest, soma XP, atualiza contador global e checa evolução."""
    quest = player["quests"][index]
    if quest["status"] == "Concluída": return

    recompensas = {"Fácil": 10, "Média": 30, "Difícil": 80}
    ganho = recompensas.get(quest["dificuldade"], 10)
    
    quest["status"] = "Concluída"
    player["xp"] += ganho
    player["total_concluido"] += 1 # Incrementa o progresso da carreira
    
    print(f"\n[SISTEMA] Quest Finalizada! +{ganho} XP.")
    print(f"[PROGRESSO] Total de Quests Concluídas: {player['total_concluido']}")

    # Lógica de Level Up
    while player["xp"] >= player["xp_proximo_nivel"]:
        player["nivel"] += 1
        player["xp"] -= player["xp_proximo_nivel"]
        print(f"⭐ LEVEL UP! Você atingiu o Nível {player['nivel']}!")

    # Após ganhar nível ou quest, checa se sobe de Rank
    verificar_ascensao_rank(player)
    salvar_dados(player)

# --- GESTÃO DE PERSONAGEM ---

def criar_personagem():
    print("\n[SISTEMA: INICIALIZANDO REGISTRO DE CAÇADOR]")
    nome = input("Qual o seu nome? ")
    
    novo_player = {
        "nome": nome,
        "rank": "E",          # Rank Inicial
        "nivel": 1,
        "xp": 0,
        "xp_proximo_nivel": 100,
        "hp": 100,
        "total_concluido": 0, # Contador de Carreira
        "ultimo_acesso": date.today(),
        "quests": []
    }
    salvar_dados(novo_player)
    return novo_player

# --- INTERFACE PRINCIPAL ---

def main():
    player = carregar_dados()
    if not player:
        player = criar_personagem()
    
    # Adicionando campos novos caso o save seja de uma versão antiga
    if "rank" not in player: player["rank"] = "E"
    if "total_concluido" not in player: player["total_concluido"] = 0

    verificar_passagem_tempo(player)
    
    while True:
        if player["hp"] <= 0:
            print("\n!!! VOCÊ FALHOU COM O SISTEMA. REGISTRO APAGADO. !!!")
            if os.path.exists(ARQUIVO_SAVE): os.remove(ARQUIVO_SAVE)
            break

        # Dashboard Estilizado
        print("\n" + "═"*45)
        print(f" CAÇADOR: {player['nome']} | RANK: [{player['rank']}]")
        print(f" LVL: {player['nivel']} | HP: {player['hp']}/100 | XP: {player['xp']}/{player['xp_proximo_nivel']}")
        print(f" TOTAL DE MISSÕES: {player['total_concluido']}")
        print("═"*45)
        print("1. Lista de Quests")
        print("2. Nova Quest Diária")
        print("3. Sair")
        
        op = input("\nEscolha sua ação: ")
        
        if op == "1":
            if not player["quests"]:
                print("\n[!] Nenhuma quest pendente.")
            else:
                for i, q in enumerate(player["quests"]):
                    print(f"{i+1}. [{q['status']}] {q['tarefa']} ({q['dificuldade']})")
                
                escolha = input("\nNº para concluir (0 para voltar): ")
                if escolha.isdigit() and int(escolha) > 0:
                    idx = int(escolha) - 1
                    if idx < len(player["quests"]):
                        concluir_quest(player, idx)
        
        elif op == "2":
            desc = input("Descrição da Quest: ")
            dif = input("Dificuldade (1:Fácil, 2:Média, 3:Difícil): ")
            grau = {"1": "Fácil", "2": "Média", "3": "Difícil"}.get(dif, "Fácil")
            player["quests"].append({"tarefa": desc, "dificuldade": grau, "status": "Pendente"})
            salvar_dados(player)
            print("[SISTEMA] Quest registrada.")
            
        elif op == "3":
            print("Sincronizando com o Sistema... Até breve.")
            break

if __name__ == "__main__":
    main()
    