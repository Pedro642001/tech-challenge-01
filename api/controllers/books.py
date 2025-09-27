from fastapi import APIRouter, HTTPException, Query, Path # crupo de rotas, error 404, url, url
from pydantic import BaseModel # os campos do livro
from typing import List, Optional #lista e campo opcional 
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "books.db") # caminho do banco de dados

router = APIRouter(prefix = "/api/v1/books", tags = ["books"])

# modelo de livro
class Book(BaseModel):
    id: int # numero
    title: str 
    price: float | str
    rating: Optional[str] = None # none vazio
    availability: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None

# conexão com o books banco conecta o banco
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Converte uma linha do banco em objeto book
def row_to_book(row: sqlite3.Row) -> Book:
    return Book(
        id = row ["id"],
        title = row ["titulo"],
        price = row ["preco"],
        rating = row ["rating"],
        availability = row ["disponibilidade"],
        category = row ["categoria"],
        image = row ["imagem"], 
    )

@router.get("", response_model = List[Book])
def list_books():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, titulo, preco, disponibilidade, rating, categoria, imagem "
            "FROM livros ORDER BY id ASC"
        ).fetchall()

    return [row_to_book(r) for r in rows]

@router.get("/{id}", response_model = Book)
def get_book(id: int = Path(..., description = "ID do livro")):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, titulo, preco, disponibilidade, rating, categoria, imagem "
            "FROM livros WHERE id = ?",
            (id,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code = 404, detail = "Book not found")
    return row_to_book(row)

@router.get("/search", response_model = List[Book])
def search_books(
        title: Optional[str] = Query(None),
        category: Optional[str] = Query(None),
):
    clauses, params = [], []
    if title:
        clauses.append("LOWER(titulo) LIKE ?")
        params.append(f"%{title.lower()}%")

    if category:
        clauses.append("LOWER(categoria) = ?")
        params.append(category.lower())

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""

    sql = (
        "SELECT id, titulo, preco, disponibilidade, rating, categoria, imagem "
        f"FROM livros {where} ORDER BY id ASC"
    )

    with get_conn() as conn:
        rows = conn.execute(sql, tuple(params)).fetchall()

    return [row_to_book(r) for r in rows]