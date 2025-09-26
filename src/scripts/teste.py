# from modules.utils.functions import trataTitulo, trataPreco, obterObjetos, obterTotalPaginasCategoria
# from config.variables import Config
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#from modules.utils.sqlite_util import SQLiteDB
from modules.utils.livro_dao import LivroDAO
from modules.utils.functions import trataTitulo, trataPreco, obterObjetos, obterTotalPaginasCategoria


if __name__ == "__main__":
    #libs = Path("/Users/christiano.sa/Trabalho/Fase1/tech-challenge-01/src").parent / 'src' / 'modules' / 'utils' / 'functions'
    #sys.path.insert(0, libs.as_posix())  # Adiciona o diretório ao sys.path para importar o módulo

    #from modules.utils.functions import trataTitulo, trataPreco, obterObjetos, obterTotalPaginasCategoria

    dados = []
    
    titulo = "titulo"
    preco = 10
    disponibilidade = "Em Estoque"
    rating = "One"
    categ = "Categoria"
    imagem = "Imagem"

    dados.append([titulo, preco, disponibilidade, rating, categ, imagem])

    
    dao = LivroDAO()
    if dao.verificar_conexao():
        print("Conexão com o banco de dados verificada com sucesso.")
        rows = dao.listar_livros()
        for row in rows:
            print(row)
  