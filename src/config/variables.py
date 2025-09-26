from pathlib import Path
import os
""""
Variáveis de configuração do projeto
"""
class Config:
    #path_files = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_files = Path(__file__).parents[1]        # Caminho raiz do projeto (dois níveis acima deste arquivo)
    libs_files = path_files / 'modules' / 'utils' # Caminho para a pasta de bibliotecas (módulos utilitários)
    data_files = path_files / 'data'              # Caminho para a pasta de dados
    db_path = './dados/banco'                     # Caminho para o arquivo do banco de dados SQLite