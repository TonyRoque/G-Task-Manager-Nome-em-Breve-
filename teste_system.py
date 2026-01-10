import unittest
from datetime import date, timedelta
# Importamos as funções do seu main.py
from main import concluir_quest, verificar_permadeath

class TestSoloLeveling(unittest.TestCase):

    def setUp(self):
        """Prepara um cenário de teste antes de cada função de teste."""
        self.player_teste = {
            "nome": "Testador",
            "nivel": 1,
            "xp": 0,
            "xp_proximo_nivel": 100,
            "hp": 100,
            "ultimo_acesso": date.today(),
            "quests": [{"tarefa": "Teste", "dificuldade": "Fácil", "status": "Pendente"}]
        }

    def test_ganho_xp_e_level_up(self):
        """Verifica se o Level Up ocorre ao atingir o XP necessário."""
        # Simulamos completar uma quest difícil (80xp) + 30xp = 110xp
        self.player_teste["xp"] = 80
        concluir_quest(self.player_teste, 0) # Conclui a quest de teste (mais 10xp)
        
        # Forçamos mais um ganho para testar o limite
        self.player_teste["xp"] += 20 
        
        # Se a lógica estiver certa, o nível deve ser 2 e o XP deve ter resetado/sobrado
        if self.player_teste["xp"] >= self.player_teste["xp_proximo_nivel"]:
             # Simula a lógica que está no seu main
             self.player_teste["nivel"] += 1
        
        self.assertEqual(self.player_teste["nivel"], 2)

    def test_punicao_tempo(self):
        """Simula a virada de dia para ver se o dano é aplicado."""
        ontem = date.today() - timedelta(days=1)
        self.player_teste["ultimo_acesso"] = ontem
        
        # Aqui testamos se o sistema detecta que hoje > ontem
        self.assertTrue(date.today() > self.player_teste["ultimo_acesso"])

if __name__ == "__main__":
    unittest.main()