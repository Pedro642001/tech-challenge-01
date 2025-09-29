""""
Script para fazer o scrapping do site https://books.toscrape.com/ e armazenar os dados em um banco de dados SQLite.
Pacotes necessários: 
    - requests (fazer as requisições protocolo web)
    - beautifulsoup4 (manuseio do HTML para extrair as informações das tags) 
    - sqlite3 (armazenamento em um banco de dados SQLite das informações extraídas)
"""
import requests
from bs4 import BeautifulSoup
import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.utils.livro_dao import LivroDAO
from modules.utils.functions import trataTitulo, trataPreco, obterObjetos, obterTotal, trataDisponibilidade
from config.variables import Config

class Scrapping:

    url = "https://books.toscrape.com/"  #site contendo catálogo de livros a ser baixado
    urlb = "https://books.toscrape.com/" #urlbase, usada para concatenar as páginas a serem importadas

    dados = [] # lista para armazenar os dados dos livros
    contador = 0 
   
    def run(self)-> int:
        urlb = self.urlb
        
        # pegar todas as categorias dentro do objeto "ul" com classe "nav nav-list"
        # o parâmretro "C" indica que queremos categorias
        categorias = obterObjetos(self.url, "C")
        qtdelivros = obterTotal(self.url, "L")      
        dados = []

        # para cada categoria, pegar os livros
        for categoria in categorias[1:2]:

            # ignorar a categoria "Books", que é a categoria geral
            if categoria.text.strip() != "Books":

                # monta a url para pegar a listagem de livros por categoria
                # a primeira parte tem a url base e a segunda parte é o href da categoria
                urlcategoria = urlb + categoria["href"]
                
                # obtem, dentro da página da categoria, o total de páginas
                # essa informação vem no topo da página, dentro de uma "ul" com classe "pager" e
                # é específica de cada categoria
                paginas = obterTotal(urlcategoria, "P")

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

                    # separar titulo, preço, disponibilidade, rating(classificação com estrelas)
                    for livro in livros:
                        titulo = trataTitulo(livro.h3.a["title"])  # remove caracteres especiais do título
                        preco = trataPreco(livro.find("p", class_="price_color").text) #.replace("Â","")
                        disponibilidade = livro.find("p", class_="instock availability").text.strip()
                        rating = livro.p["class"][1]  # o rating vem como classe: ["star-rating", "Three"]
                        categ = categoria.text.strip()
                        imagem = livro.img["src"].replace("../../../../", urlb) # url da imagem do livro
                        
                        print(f"Importando livro: {titulo}, {self.contador} de {qtdelivros} ")
                        urllivro = livro.a["href"].replace("../../../", urlb + "catalogue/") # url do livro
                        tabeladetalheslivro = obterObjetos(urllivro, "D") # obtem os detalhes do livro
                        all_tds = tabeladetalheslivro.find_all('td')
                        i = 0
                        for detalhe in all_tds:
                            i = i + 1
                            if i == 1: #upc
                                upc = detalhe.text # obtem o UPC do livro
                            elif i == 6: #availability
                                disponibilidade = trataDisponibilidade(detalhe.text)[0] # obtem a disponibilidade do livro
                        
                        self.contador = self.contador + 1

                        dados.append([upc, titulo, preco, disponibilidade, rating, categ, imagem])

            
        """"
        Inatancia a classe LivroDAO, responsável pela persistência dos dados de livros na base 
        e chamo o método salvar_livros para salvar os dados no banco de dados SQLite
        """
        dao = LivroDAO()
        return dao.salvar_livros(dados)
 