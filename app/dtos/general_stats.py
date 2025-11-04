from typing import List

from pydantic import BaseModel, Field


class RatingRange(BaseModel):
    range: str = Field(..., example="4-5", description="Faixa de avaliação (por exemplo, '4-5')")
    count: int = Field(..., example=120, description="Quantidade de livros dentro dessa faixa")


class GeneralStatsDto(BaseModel):
    total_books: int = Field(..., example=350, description="Número total de livros cadastrados")
    average_price: float = Field(..., example=42.75, description="Preço médio dos livros")
    rating_distribution: List[RatingRange] = Field(
        ...,
        example=[
            {"range": "0-1", "count": 25},
            {"range": "1-2", "count": 110},
            {"range": "2-3", "count": 215},
        ],
        description="Distribuição de avaliações dos livros",
    )
