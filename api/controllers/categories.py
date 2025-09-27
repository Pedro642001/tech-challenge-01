from fastapi import APIRouter
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "books.db")

router = APIRouter(prefix = "/api/v1/categories", tags = ["categories"])

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("", response_model = list[str])
def list_categories():
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT DISTINCT categoria
            FROM livros
            WHERE categoria IS NOT NULL AND TRIM(categoria) <> ''
            ORDER BY categoria COLLATE NOCASE ASC
            """
        ).fetchall()

    return [r["categoria"] for r in rows]    