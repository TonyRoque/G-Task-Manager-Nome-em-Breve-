# ⚔️ Task Manager (V0.3) - [Nome em Breve]

> **Status:** Versão 0.3 estável com Sistema de Ranks e Testes Automatizados.

Este é um gerenciador de tarefas gamificado desenvolvido em Python para o terminal Linux. O objetivo é transformar a produtividade em uma jornada de evolução.

> **O ponto central:** Não é apenas marcar tarefas concluídas. É um sistema para te tirar do modo automático e te obrigar a cumprir o que prometeu a si mesmo. É sobre perguntar a si mesmo o que esta fazendo, e se esta fazendo aquilo que gostaria e prometeu que faria.

## 📝 O Sistema
Diferente de listas comuns, aqui há consequências. O fracasso consome seu **HP**. Se o HP zerar, o sistema executa o **Permadeath**: seu save é deletado. 

*O gatilho é simples: Se hoje fosse seu ultimo dia, estaria satisfeito? Fez o que queria fazer, cumpriu as coisas que prometeu?

## 🛠️ Tecnologias e Estudos
- **Python:** Lógica principal e dicionários.
- **JSON:** Persistência de dados (meu primeiro passo antes de chegar em Bancos de Dados SQL).
- **Linux Terminal:** Interface focada em minimalismo e agilidade.

11/01/2026
## 🚀 Funcionalidades Atuais
- [x] **Cadastro:** Registro inicial do Caçador.
- [x] **Quests Diárias:** 3 níveis de dificuldade com ganhos proporcionais de XP.
- [x] **Tempo é um aliado:** Lógica de tempo que pune a procrastinação entre acessos.
- [x] **Sistema de Ranks:** Portões de evolução baseados em Nível e Total de Quests.
- [x] **Persistência:** Dados salvos em JSON com normalização de data ISO.
- [x] **Testes:** Scripts de testes unitários (`unittest`) para garantir a integridade do HP e XP.

## 🛠️ Melhorias (Pensando...)


### 🛡️ Engenharia e Robustez (Alta Prioridade)
- [ ] **Tratamento de Exceções** Implementar blocos `try/except` para lidar com erros de leitura de arquivo (I/O) e JSON corrompido.
- [ ] **Validação de Inputs** Blindar o terminal contra entradas inválidas (ex: digitar letras em campos numéricos).
- [ ] **Curva de XP Dinâmica** Substituir o XP fixo (100) por uma fórmula de escalonamento (Scaling).
- [ ] **Sanitização de Datas** Padronizar objetos `date` e `datetime` para evitar crashes na serialização.

### ✨ Novas Funcionalidades (Próximas Versões)
- [ ] **Quests de Longo Prazo:** Implementação de metas Mensais e Trimestrais (Metas Financeiras/Vida).
- [ ] **Modularização:** Separar o código em `database.py`, `logic.py` e `ui.py`.(Vai demorar)
- [ ] **Histórico de Logs:** Arquivo de log para registrar quests falhas e sucessos passados.

## 🧠 Aprendizados Técnicos
Este projeto é um laboratório de estudos onde aplico:
* Manipulação de arquivos e persistência de dados.
* Lógica de tempo com o módulo `datetime`.
* Versionamento de código com Git/GitHub.
* Testes Automatizados para garantia de qualidade.