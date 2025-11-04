from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class CategoryDto(BaseModel):
    id: int = Field(..., example=9)
    name: str = Field(..., example="Fiction")
    link: HttpUrl = Field(
        ...,
        example="https://books.toscrape.com/catalogue/category/books/fiction_10/index.html",
        description="URL da categoria do livro.",
    )
    created_at: datetime = Field(..., example="2025-10-20T23:12:39.958580Z")
    updated_at: datetime = Field(..., example="2025-10-20T23:12:39.958589Z")
