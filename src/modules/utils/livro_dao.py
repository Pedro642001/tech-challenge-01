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
    # Define o caminho para o novo diretório
    path_db = Path(Config.db_path)

    # Cria o diretório e quaisquer diretórios pais ausentes
    path_db.mkdir(parents=True, exist_ok=True)

    #db_connection = None

    # ao instanciar a classe, abre uma conexão com o banco de dados SQLite
    # def __init__(self):
    #     if LivroDAO.db_connection is None:
    #         try:
    #             print(self.path_db.as_posix())
    #             self.db_connection = sqlite3.connect(self.path_db / "book.db") #self.db_path)
    #         except sqlite3.Error as e:
    #             print(f"Erro ao conectar ao banco de dados: {e}")
    #             sys.exit(1) 
    #         finally:
    #             if self.db_connection:
    #                 #print(self.db_path.as_posix())
    #                 print("Conexão com o banco de dados SQLite estabelecida com sucesso.")
    
    def verificar_conexao(self)-> bool:
        retorno = False
        try:
            # Tenta estabelecer a conexão com o banco de dados
            conn = sqlite3.connect(self.path_db / "book.db")

            #Criar um cursor e executar uma pequena consulta para verificar a funcionalidade
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) from livros ") # Uma consulta simples que não deve falhar
            resultado = cursor.fetchone()

            if resultado[0] != 0:
                retorno = True  # Conexão e consulta bem-sucedidas
            else:
                retorno = False # A consulta não retornou o resultado esperado
        except sqlite3.Error as e:
            # Captura qualquer erro relacionado ao SQLite e o imprime
            retorno = False
        finally:
            # Garante que a conexão seja fechada, mesmo que ocorra um erro
            if 'conn' in locals() and conn:
                conn.close()
        return retorno
        
    def salvar_livros(self, dados)-> int:    

        # recupero uma conexão com banco de dados SQLite
        conn =  sqlite3.connect(self.path_db / "book.db")
        cursor = conn.cursor()
        try:
            # Cria a tabela livros se não existir
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS livros (
                            upc TEXT PRIMARY KEY,
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
                            INSERT INTO livros (upc, titulo, preco, disponibilidade, rating, categoria, imagem)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', dados)
            conn.commit()

            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao salvar livros no banco de dados: {e}")

        return len(dados)

    def obter_livro(self, id: int):
        conn = sqlite3.connect(self.path_db / "book.db")
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM livros WHERE id = ?", (id, ))
        return mycursor.fetchone()

    def listar_livros(self) -> list:
        conn = sqlite3.connect(self.path_db / "book.db")
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