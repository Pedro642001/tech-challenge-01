from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from app.dtos.category import CategoryDto


class BookDto(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="My Name Is Lucy Barton")
    description: str = Field(..., example="A novel about love, family, and redemption...")
    url: HttpUrl = Field(
        ...,
        example="https://books.toscrape.com/catalogue/my-name-is-lucy-barton_720/index.html",
        description="Link para a página do livro.",
    )
    image_url: HttpUrl = Field(
        ...,
        example="https://books.toscrape.com/media/cache/28/db/28db43984c765a1d02fd3495f5c52eb6.jpg",
        description="URL da imagem de capa do livro.",
    )
    price: float = Field(..., example=41.56)
    rating: int = Field(
        ..., ge=1, le=5, example=1, description="Avaliação do livro (1 a 5 estrelas)."
    )
    category: CategoryDto
    created_at: datetime = Field(..., example="2025-10-20T23:13:18.768042Z")
    updated_at: datetime = Field(..., example="2025-10-20T23:13:18.768079Z")
