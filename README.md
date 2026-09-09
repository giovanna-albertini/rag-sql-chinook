# RAG + SQL — Natural Language to SQL

Projeto de **AI Engineering aplicado a dados relacionais**. A aplicação recebe uma pergunta em linguagem natural, utiliza um LLM para gerar SQL restrito ao schema do banco Chinook, executa a consulta localmente e transforma o resultado em uma resposta compreensível.

## Arquitetura

```text
Pergunta do usuário
        ↓
Contexto do schema
        ↓
LLM / Text-to-SQL
        ↓
Validação da SQL
        ↓
SQLite / Chinook
        ↓
Resultado estruturado
        ↓
Resposta em linguagem natural
```

## Tecnologias

- Python 3.10+
- OpenAI API
- SQLite / sqlite3
- Prompt Engineering
- Docker (estrutura preparada)
- python-dotenv

## Exemplo de caso de uso

**Pergunta:** Qual artista gerou mais receita para a loja?

O pipeline transforma a intenção em uma consulta compatível com o schema, executa a SQL e usa apenas o resultado retornado para compor a resposta.

## Segurança

O projeto foi desenvolvido para **banco SQLite local de demonstração**. Em ambientes reais, uma arquitetura Text-to-SQL deve utilizar usuário read-only, allowlist de comandos, limites de execução, validação da query e observabilidade.

O argumento `--dry-run` permite inspecionar a SQL antes da execução.

## Execução

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sua_chave"
python -m src.rag_sql_chinook.main --query "Qual artista gerou mais receita para a loja?"
```

Banco esperado: `data/Chinook_Sqlite.sqlite`.

## Estrutura

```text
rag-sql-chinook/
├── src/
├── notebooks/
├── data/
├── docker/
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Próximas evoluções

- validação estrutural de SQL com parser;
- bloqueio explícito de DDL/DML;
- testes automatizados;
- FastAPI;
- Docker executável;
- tracing e avaliação de qualidade das respostas.

## Competências demonstradas

`LLMs` · `Text-to-SQL` · `Python` · `SQL` · `Prompt Engineering` · `AI Engineering` · `Data Engineering`
