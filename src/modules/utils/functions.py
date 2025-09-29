import re 
import requests
from bs4 import BeautifulSoup

def trataTitulo(texto) -> str:
    """
    Remove caracteres não ASCII de uma string.
    :param texto: A string de entrada.
    
    :return: A string sem caracteres não ASCII.
    """
    return re.sub(r'[^\x00-\x7F]+', '', texto)

def trataPreco(price: str) -> float:
    """
    Trata uma string de preço, removendo o símbolo de moeda e convertendo para float.
    :param price: A string de preço (ex: '£51.77').
    
    :return: O preço como float (ex: 51.77).
    """
    try:
        # Remove o símbolo de libra e qualquer caractere especial, retornando como string
        texto = float(price.replace('£', '').replace('Â', '').strip())  
    except ValueError:
        # Código a ser executado se ocorrer um ValueError
        print("Erro: Valor inválido para conversão de preço!")
        texto = 0.0

    return texto

def trataDisponibilidade(texto)->int:
    numeros = re.findall(r'\d+', texto)  # Encontra todos os grupos de dígitos
    return [int(num) for num in numeros]

def obterObjetos(url: str, tipo: str) -> list:
    """
    Extrai lista de um objeto BeautifulSoup.
    :param url: URL para obter o conteúdo do BeautifulSoup contendo o HTML da página.
    :tipo: Tipo de lista a ser extraída (pode ser "C" para categoria ou "L" para livros).
    :return: Lista de de objetos encontradas.
    """
    try:
        request = requests.get(url, timeout = 30) # baixa o html do site
        request.raise_for_status() # se não for 200 levanta erro
        soup = BeautifulSoup(request.text, "html.parser") # parser é como se fosse um leitor de html
    except requests.RequestException as e:
        print(f"Erro ao obter informações da URL: {e}")
        lista = []
    finally:
        if tipo == "C":
            # pegar todas as categorias do menu lateral, 
            # que estão na ul com classe "nav nav-list"
            lista = soup.find("ul", class_="nav nav-list").find_all("a")
        elif tipo == "L":
            # pegar todos os livros
            lista = soup.find_all("article", class_="product_pod")
        elif tipo == "D":
            # pegar os detalhes do livro
            specific_table = soup.find("table", class_="table table-striped")
            lista = specific_table
        else:
            lista = []
            

    return lista

def obterTotal(urlcateg: str, tipo: str) -> int:
    """
    Obtém o total de páginas de uma categoria a partir da URL da categoria.
    :param urlcateg: URL da categoria para obter o total de páginas.
    :return: Total de páginas na categoria.
    """
    try:
        # abre a página de uma categoria, pegando todos os livros de uma determinada categoria
        request = requests.get(urlcateg, timeout = 30) # baixa o html do site
        request.raise_for_status() # se não for 200 levanta erro
        soup = BeautifulSoup(request.text, "html.parser") 
        
        # pegar o total de livros
        total = soup.find("form", class_="form-horizontal").find("strong").text # Extract the text content
    except requests.RequestException as e:
        print(f"Erro ao obter informações da URL: {e}")
        total = 0
    finally:
        if tipo == "P": # calcula o total de páginas 
            if total != 0:
                retorno = (int(total)//20)+1
            else:
                retorno = 0
        else:
            if tipo == "L":
                retorno = int(total)

    return retorno