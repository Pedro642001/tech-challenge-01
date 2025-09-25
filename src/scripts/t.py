from pathlib import Path
import sys
import modules.utils.functions 

if __name__ == "__main__":
    libs = Path("/Users/christiano.sa/Trabalho/Fase1/tech-challenge-01/src").parent / 'src' / 'modules' / 'utils' / 'functions'
    sys.path.insert(0, libs.as_posix())  # Adiciona o diretório ao sys.path para importar o módulo
