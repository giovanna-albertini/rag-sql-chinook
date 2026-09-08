#!/usr/bin/env python3
"""
RAG SQL for Chinook — CLI pipeline
- --query: pergunta em linguagem natural
- --db: caminho para banco SQLite
- --dry-run: mostra a SQL gerada sem executar
"""
import os
import argparse
import logging
import sqlite3
from dataclasses import dataclass
from typing import List, Tuple

import openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Schema context used to constrain the SQL generator
SCHEMA_CONTEXT = """
Você é um especialista em SQL para um banco SQLite chamado Chinook.
Chinook representa uma loja digital de música (como iTunes).

Tabelas disponíveis:

  Artist       (ArtistId, Name)
  Album        (AlbumId, Title, ArtistId)
  Track        (TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
  Genre        (GenreId, Name)
  MediaType    (MediaTypeId, Name)
  Customer     (CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId)
  Employee     (EmployeeId, LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Country, PostalCode, Phone, Fax, Email)
  Invoice      (InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total)
  InvoiceLine  (InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity)
  Playlist     (PlaylistId, Name)
  PlaylistTrack(PlaylistId, TrackId)

Regras:
- Use apenas SQLite syntax
- Para extrair ano de datas use: strftime('%Y', InvoiceDate)
- Retorne APENAS o SQL quando solicitado (sem explicações)
"""

@dataclass
class Settings:
    openai_api_key: str = os.environ.get('OPENAI_API_KEY', '')
    model_sql: str = os.environ.get('OPENAI_SQL_MODEL', 'gpt-3.5-turbo')
    model_nl: str = os.environ.get('OPENAI_NL_MODEL', 'gpt-3.5-turbo')

settings = Settings()

# Ensure OpenAI is configured
if settings.openai_api_key:
    openai.api_key = settings.openai_api_key
else:
    logger.warning('OPENAI_API_KEY não definida. Chamadas ao LLM podem falhar.')


def pergunta_para_sql(pergunta: str) -> str:
    """Gera uma query SQL a partir da pergunta usando o LLM.
    Retorna apenas o SQL (string).
    """
    messages = [
        {"role": "system", "content": SCHEMA_CONTEXT},
        {"role": "user", "content": f"Gere SQL para: {pergunta}"}
    ]
    try:
        resp = openai.ChatCompletion.create(
            model=settings.model_sql,
            messages=messages,
            temperature=0.0,
            max_tokens=512
        )
        sql = resp['choices'][0]['message']['content'].strip()
        return sql
    except Exception as e:
        logger.error('Erro ao gerar SQL: %s', e)
        raise


def executar_sql(db_path: str, sql: str) -> Tuple[List[str], List[Tuple]]:
    """Executa a query no banco SQLite local e retorna (colunas, linhas)."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f'Banco não encontrado: {db_path}')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        return cols, rows
    finally:
        conn.close()


def dados_para_resposta(pergunta: str, colunas: List[str], linhas: List[Tuple]) -> str:
    """Usa o LLM para transformar dados brutos em resposta em linguagem natural."""
    if not linhas:
        return 'Nenhum dado encontrado para essa pergunta.'
    dados = "\n".join(str(dict(zip(colunas, linha))) for linha in linhas)
    messages = [
        {"role": "system", "content": "Você é um analista de dados de uma loja de música digital. Responda em português com clareza e objetividade."},
        {"role": "user", "content": f"Pergunta: {pergunta}\n\nDados:\n{dados}\n\nResponda a pergunta com base nesses dados."}
    ]
    try:
        resp = openai.ChatCompletion.create(
            model=settings.model_nl,
            messages=messages,
            temperature=0.7,
            max_tokens=512
        )
        answer = resp['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        logger.error('Erro ao gerar resposta em NL: %s', e)
        raise


def main():
    parser = argparse.ArgumentParser(description='RAG SQL Chinook — pergunta → SQL → execução → resposta')
    parser.add_argument('--db', type=str, default='data/Chinook_Sqlite.sqlite', help='Caminho para o arquivo SQLite')
    parser.add_argument('--query', type=str, help='Pergunta em linguagem natural')
    parser.add_argument('--dry-run', action='store_true', help='Mostra a SQL gerada sem executar')
    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        return

    print('\n' + '='*70)
    print(f'❓ Pergunta: {args.query}')
    print('='*70 + '\n')

    sql = pergunta_para_sql(args.query)
    print('--- SQL gerada ---')
    print(sql)

    if args.dry_run:
        print('\nDry-run: não será executada.')
        return

    try:
        colunas, linhas = executar_sql(args.db, sql)
    except Exception as e:
        print(f'Erro ao executar SQL: {e}')
        return

    resposta = dados_para_resposta(args.query, colunas, linhas)
    print('\n=== Resposta ===')
    print(resposta)

if __name__ == '__main__':
    main()
