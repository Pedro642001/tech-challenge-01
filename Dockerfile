FROM python:3.13-slim

# Instala o Poetry
RUN pip install --no-cache-dir poetry==2.2.1

# Define o diretório de trabalho
WORKDIR /code

# Copia os arquivos de dependências
COPY pyproject.toml poetry.lock ./

# Instala as dependências do projeto
RUN poetry install --without dev --no-root --no-interaction --no-ansi

# Copia o código da aplicação
COPY ./app ./app

# Observa a porta que a aplicação irá rodar
EXPOSE 8000

# Comando padrão
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]