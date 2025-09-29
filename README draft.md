# Projeto Fase 1, FIAP

Este projeto foi o resultado do trabalho desenvolvido pelo grupo 01 do curso 7MLET da FIAP. A ideia é montar uma base de dados contendo livros cadastrados e permitir a consulta deles através de API's. Tudo desenvolvido em Python. O escopo ficou dividido em em duas partes. A primeira tem como objetivo montar a infraestrutura de extração dos dados, que foi implementada através de um script python que realiza **web scraping** no site https://books.toscrape.com/. A segunda etapa corresponde no desenvolvimento e disponibilização de API's públicas para que cientistas de dados e usuários interessados possam usar esses dados com facilidade.

Uma pipeline completo de dados, com API pública para servir esses dados, pensando em escalabilidade e reusabilidade está disponível (seguindo o desenho de arquitetura destacado)

Ele foi organizado em três arquivos principais:
- `functions.py`: Contém funções auxiliares usadas no scraping.
- `livro_dao.py`: Responsável por interações com armazenamento/manipulação dos dados (ex: SQLite).
- `scrapping.py`: Script principal para executar o web scraping.

O repositório onde o código está disponibilizado encontra-se no github.

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
---

### 2.3. Instalar as dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install requests 
pip install beautifulsoup4
pip install flask
pip install flask_jwt_extended
pip install flask_bcrypt
pip install flask_sqlalchemy
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

## 4. Como testar usando o Postman
Boa! 🚀 O **Postman** é uma das formas mais práticas de testar APIs JWT. Vou te mostrar o passo a passo para testar o seu app Flask que criamos:

---

## 🔹 1. Preparar ambiente

* Abra o **Postman** (desktop ou versão web).
* Crie uma **Collection** chamada `API Flask JWT`.
* Dentro dela, crie as requisições que vamos usar.

---

## 🔹 2. Criar usuário (`/register`)

1. Clique em **New Request** → nomeie `Register`.
2. Método: `POST`
   URL: `http://127.0.0.1:5000/register`
3. Aba **Body** → escolha **raw** → **JSON**.
4. Insira:

   ```json
   {
     "username": "alice",
     "password": "senha123",
     "role": "admin"
   }
   ```
5. Clique em **Send**.
   → Deve retornar `{"msg": "usuário criado com sucesso"}`.

---

## 🔹 3. Login (`/login`)

1. Nova request: `Login`.
2. Método: `POST`
   URL: `http://127.0.0.1:5000/login`
3. Aba **Body → raw → JSON**:

   ```json
   {
     "username": "alice",
     "password": "senha123"
   }
   ```
4. Clique em **Send**.
   → Vai retornar algo assim:

   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
   }
   ```

⚡ Copie o valor de `access_token`.

---

## 🔹 4. Acessar rota protegida (`/profile`)

1. Nova request: `Profile`.
2. Método: `GET`
   URL: `http://127.0.0.1:5000/profile`
3. Aba **Headers** → adicione:

   ```
   Key: Authorization
   Value: Bearer SEU_ACCESS_TOKEN
   ```
4. Clique em **Send**.
   → Deve retornar:

   ```json
   {"msg": "Olá, alice. Esta é sua profile."}
   ```

---

## 🔹 5. Testar refresh token (`/refresh`)

1. Nova request: `Refresh`.
2. Método: `POST`
   URL: `http://127.0.0.1:5000/refresh`
3. Aba **Headers** → adicione:

   ```
   Key: Authorization
   Value: Bearer SEU_REFRESH_TOKEN
   ```
4. Clique em **Send**.
   → Deve retornar um novo `access_token`.

---

## 🔹 6. Logout (`/logout`)

1. Nova request: `Logout`.
2. Método: `DELETE`
   URL: `http://127.0.0.1:5000/logout`
3. Aba **Headers** → adicione:

   ```
   Key: Authorization
   Value: Bearer SEU_ACCESS_TOKEN
   ```
4. Clique em **Send**.
   → Deve retornar:

   ```json
   {"msg": "token revogado (logout) com sucesso"}
   ```

Se tentar usar o mesmo token de novo em `/profile`, vai dar erro **401 (Token has been revoked)** ✅

---

## 🔹 7. Dica extra: usar **Variables** no Postman

Em vez de copiar/colar o token toda hora, você pode:

1. Salvar o `access_token` da resposta do login em uma **variable** chamada `{{access_token}}`.
2. Configurar o header `Authorization` como:

   ```
   Bearer {{access_token}}
   ```

Assim o Postman atualiza automaticamente depois do login.

---



