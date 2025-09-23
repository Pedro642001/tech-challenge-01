from os import write
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from os import replace
import sqlite3
from pathlib import Path
from modules.utils.functions import trataTitulo, trataPreco, obterObjetos, obterTotalPaginasCategoria
from config.variables import Config


libs = Path(Config.libs_files).parent / 'utils' / 'functions'
sys.path.insert(0, libs.as_posix())  # Adiciona o diretório ao sys.path para importar o módulo



url = "https://books.toscrape.com/"  #site contendo catálogo de livros a ser baixado
urlb = "https://books.toscrape.com/" #urlbase, usada para concatenar as páginas a serem importadas


dados = [] # lista para armazenar os dados dos livros

# pegar todas as categorias dentro do objeto "ul" com classe "nav nav-list"
# o parâmretro "C" indica que queremos categorias
categorias = obterObjetos(url, "C")

# para cada categoria, pegar os livros
for categoria in categorias:

    # ignorar a categoria "Books", que é a categoria geral
    if categoria.text.strip() != "Books":
        print("Obtendo os livros da categoria:", categoria.text.strip())

        # monta a url para pegar a listagem de livros por categoria
        # a primeira parte tem a url base e a segunda parte é o href da categoria
        urlcategoria = urlb + categoria["href"]
        
        # obtem, dentro da página da categoria, o total de páginas
        # essa informação vem no topo da página, dentro de uma "ul" com classe "pager" e
        # é específica de cada categoria
        paginas = obterTotalPaginasCategoria(urlcategoria)

        # para cada página da categoria, pegar os livros
        for i in range(1,(paginas+1)):
            """"
            Monta a URL da página da categoria. A primeira página foge o padrão de formação da URL das demais páginas e por isso tem um tratmento diferenciado.
            Primeira página: https://books.toscrape.com/catalogue/category/books/mystery_3/index.html
            Segunda página: https://books.toscrape.com/catalogue/category/books/mystery_3/page-2.html
            terceira página: https://books.toscrape.com/catalogue/category/books/mystery_3/page-3.html
            """
            if i != 1:  # a primeira página tem uma url diferente das páginas seguintes e por isso tem um tratamento separado
                urlcategoria = urlb + categoria["href"].replace("index.html", f"page-{i}.html")
            
            # pegar todos os livros
            # a função abaixo retorna uma lista de objetos "article" com classe "product_pod"
            # o parâmetro "L" indica que queremos livros
            livros = obterObjetos(urlcategoria, "L")
            print(f"Livros encontrados na página {i}: {len(livros)}")

            # separar titulo, preço, disponibilidade, rating(classificação com estrelas)
            for livro in livros:
                titulo = trataTitulo(livro.h3.a["title"])  # remove caracteres especiais do título
                preco = trataPreco(livro.find("p", class_="price_color").text) #.replace("Â","")
                disponibilidade = livro.find("p", class_="instock availability").text.strip()
                rating = livro.p["class"][1]  # o rating vem como classe: ["star-rating", "Three"]
                categ = categoria.text.strip()
                imagem = livro.img["src"].replace("../../../../", urlb) # url da imagem do livro

                dados.append([titulo, preco, disponibilidade, rating, categ, imagem])

# abro uma conexão com banco de dados SQLite
conn = sqlite3.connect(Config.db_path)
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

cursor.execute('SELECT categoria, count(*) FROM livros GROUP BY categoria')
grupos = cursor.fetchall()
for grupo in grupos:
    print(grupo)

conn.close()
