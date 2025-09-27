from fastapi import  FastAPI
from .controllers import health_check, books, categories

app = FastAPI(title="Tech Challenge 01", version="0.1.0")

app.include_router(health_check.router, tags=["health"])
app.include_router(books.router)
app.include_router(categories.router)