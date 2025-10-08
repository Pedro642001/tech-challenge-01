from pydantic import BaseModel


class CategoryInsightDto(BaseModel):
    name: str
    total_books: int
    average_price: float
    min_price: float
    max_price: float
