from pydantic import BaseModel, Field


class CategoryStatsDto(BaseModel):
    name: str = Field(..., description="Nome da categoria", example="Humor")
    total_books: int = Field(..., description="Total de livros na categoria", example=10)
    average_price: float = Field(..., description="Preço médio dos livros", example=33.5)
    min_price: float = Field(..., description="Preço mínimo encontrado", example=11.83)
    max_price: float = Field(..., description="Preço máximo encontrado", example=55.5)
