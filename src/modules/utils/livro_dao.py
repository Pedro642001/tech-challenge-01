"""
Módulo DAO (Data Access Object) para manipulação de dados de livros em um banco de dados SQLite.
"""
import sqlite3
import sys
import os
from pathlib import Path

# Ajusta o sys.path para importar o módulo Config. Necessário para evitar problemas de importação.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/config')
# Ajusta o sys.path para importar o módulo SQLiteDB. Necessário para evitar problemas de importação.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/modules')

from config.variables import Config

""""
Classe LivroDAO para operações de banco de dados relacionadas a livros.
"""
class LivroDAO:
    db_path = Config.db_path
    db_connection = None

    # ao instanciar a classe, abre uma conexão com o banco de dados SQLite
    def __init__(self):
        if LivroDAO.db_connection is None:
            LivroDAO.db_connection = sqlite3.connect(self.db_path)

    # m
    def salvar_livros(self, dados):    

        # recupero uma conexão com banco de dados SQLite
        conn =  LivroDAO.db_connection 
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS livros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT,
                        preco REAL,
                        disponibilidade TEXT,
                        rating TEXT,
                        categoria TEXT,
                        imagem TEXT 
                    )
                 ''')
        cursor.execute('DELETE FROM livros')  # Limpa a tabela antes de inserir novos dados
        cursor.executemany('''
                        INSERT INTO livros (titulo, preco, disponibilidade, rating, categoria, imagem)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', dados)
        conn.commit()

        conn.close()

    def obter_livro(self, id: int):
        conn = LivroDAO.db_connection
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM livros WHERE id = ?", (id, ))
        return mycursor.fetchone()

    def listar_livros(self) -> list:
        conn = LivroDAO.db_connection
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM livros")
        return mycursor.fetchall()


# • GET /api/v1/books: lista todos os livros disponíveis na base de dados.
# • GET /api/v1/books/{id}: retorna detalhes completos de um livro
# específico pelo ID.
# • GET /api/v1/books/search?title={title}&category={category}: busca
# livros por título e/ou categoria.
# • GET /api/v1/categories: lista todas as categorias de livros disponíveis.
# • GET /api/v1/health: verifica status da API e conectividade com os
# dados.