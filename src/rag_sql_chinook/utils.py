"""
Utils for rag_sql_chinook (small helpers)
"""
from typing import List, Tuple


def format_rows(colunas: List[str], linhas: List[Tuple]) -> str:
    if not linhas:
        return ''
    return '\n'.join(str(dict(zip(colunas, linha))) for linha in linhas)
