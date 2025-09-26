# Projeto Fase 1, FIAP

Este projeto foi o resultado do trabalho desenvolvido pelo grupo 01 do curso 7MLET da FIAP. A ideia é montar uma base de dados contendo livros cadastrados e permitir a consulta deles através de API's. Tudo desenvolvido em Python. O escopo ficou dividido em em duas partes. A primeira tem como objetivo montar a infraestrutura de extração dos dados, que foi implementada através de um script python que realiza **web scraping** no site https://books.toscrape.com/. A segunda etapa corresponde no desenvolvimento e disponibilização de API's públicas para que cientistas de dados e usuários interessados possam usar esses dados com facilidade.

Uma pipeline completo de dados, com API pública para servir esses dados, pensando em escalabilidade e reusabilidade está disponível (seguindo o desenho de arquitetura destacado)

Ele foi organizado em três arquivos principais:
- `functions.py`: Contém funções auxiliares usadas no scraping.
- `livro_dao.py`: Responsável por interações com armazenamento/manipulação dos dados (ex: SQLite).
- `scrapping.py`: Script principal para executar o web scraping.

Você tem duas opções para rodar o script para baixa dos dados de livros. Pode baixar o projeto, abrindo no vscode, configurando o ambiente (conforme tutorial abaixo) ou abrir o executável scrapping.pkg localizado no diretório "dist". 

repositório no git: https://github.com/Pedro642001/tech-challenge-01
---

## 1. Pré-requisitos

Antes de rodar o projeto, você precisará ter instalado:

1. **Python 3.10 ou superior**  
   👉 [Baixar Python](https://www.python.org/downloads/)

2. **Visual Studio Code (VS Code)**  
   👉 [Baixar VS Code](https://code.visualstudio.com/)

3. **Git** (opcional, mas recomendado para versionamento)  
   👉 [Baixar Git](https://git-scm.com/downloads)

⚠️ No Windows, durante a instalação do Python, marque a opção **"Add Python to PATH"**.
---

## 2. Configuração do Ambiente

### 2.1. Clonar o repositório 
git clone https://github.com/Pedro642001/tech-challenge-01
cd tech-challenge-01

### 2.2. Criar um ambiente virtual
No terminal do VS Code (ou Prompt de Comando/PowerShell no Windows):

```bash
# Windows
python -m venv venv

# macOS / Linux
python3 -m venv venv
```

Ativar o ambiente virtual:

```bash
# Windows (PowerShell)
path\to\venv\Scripts\Activate.ps1

# Windows (cmd)
path\to\venv\Scripts\activate.bat

# macOS / Linux
source path/to/venv/bin/activate
```

Você verá algo assim no terminal:
```
(venv) $
```
---

### 2.3. Instalar as dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install requests 
pip install beautifulsoup4
```
---

## 3. Executando o Script
Com o ambiente virtual ativado:

```bash
python scrapping.py
```

Se for Linux/Mac:

```bash
python3 scrapping.py
```

---

## 4. Estrutura do Projeto

```
📂 tech-challenge-01/
> api
> buid
> dados
  > banco
    ┣ 📜 book.db           # BD com os livros extraidos
> dist 
    ┣ 📜 scrapping.pkg     # Executável que baixa os dados para a base 
> doc
> src
   > modules
   > scripts
 ┗ 📜 README.md            # Documentação do projeto
```

---


