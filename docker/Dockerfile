FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "src.rag_sql_chinook.main", "--query", "Qual artista gerou mais receita para a loja?"]
