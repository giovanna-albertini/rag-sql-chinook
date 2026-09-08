from dataclasses import dataclass
import os

@dataclass
class Settings:
    openai_api_key: str = os.environ.get('OPENAI_API_KEY', '')
    openai_sql_model: str = os.environ.get('OPENAI_SQL_MODEL', 'gpt-3.5-turbo')
    openai_nl_model: str = os.environ.get('OPENAI_NL_MODEL', 'gpt-3.5-turbo')

settings = Settings()
