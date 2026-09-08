# RAG com SQL — Chinook SQLite (Perguntas → SQL → Execução → Resposta)

Descrição
--------
Pipeline RAG para um banco SQLite (Chinook). Recebe perguntas em linguagem natural, gera uma query SQL restrita ao schema do banco, executa a query localmente no SQLite e retorna uma resposta em linguagem natural baseada nos resultados.

Principais tecnologias
----------------------
- Python 3.10+
- OpenAI (API Chat completions)
- sqlite3 (biblioteca padrão do Python)
- Docker (opcional)

Instalação
---------
1. Clone o repositório:
   git clone https://github.com/giovanna-albertini/rag-sql-chinook.git
2. Crie e ative um ambiente virtual:
   python -m venv .venv
   source .venv/bin/activate
3. Instale dependências:
   pip install -r requirements.txt
4. Coloque o arquivo Chinook SQLite em `data/` (nome esperado: `Chinook_Sqlite.sqlite`) e configure sua chave:
   export OPENAI_API_KEY="sua_chave_aqui"

Uso
---
- Executar uma pergunta (padrão usa data/Chinook_Sqlite.sqlite):
  python -m src.rag_sql_chinook.main --query "Qual artista gerou mais receita para a loja?"

Argumentos úteis
----------------
- --db PATH    : caminho para o arquivo SQLite (padrão: data/Chinook_Sqlite.sqlite)
- --query TEXT : pergunta em linguagem natural a ser convertida e executada
- --dry-run    : mostra a SQL gerada sem executar

Boas práticas
------------
- Não commite chaves de API. Use variáveis de ambiente ou Secrets do CI.
- Revise a SQL gerada antes de executar em bancos de produção. Este projeto assume uso em banco local somente.

Licença
-------
MIT (padrão)
