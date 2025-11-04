from pydantic import BaseModel, Field


class BookFeatureDto(BaseModel):
    title: str = Field(..., description="Título do livro", example="My Name Is Lucy Barton")
    price: float = Field(..., description="Preço do livro", example=41.56)
    rating: int = Field(..., description="Avaliação do livro (1 a 5)", example=3)
    category: str = Field(..., description="Categoria do livro", example="Fiction")


class TrainingDataDto(BaseModel):
    features: list[list[float]] = Field(
        ...,
        description="Lista de vetores de características (X) usadas como entrada para o modelo.",
        example=[[1.0], [3.0], [1.0]],
    )

    labels: list[float] = Field(
        ...,
        description="Lista de valores esperados (y) correspondentes às saídas do modelo.",
        example=[41.56, 24.48, 40.36],
    )


class PredictionInputDto(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Avaliação do livro (1 a 5)")


class PredictionOutputDto(BaseModel):
    predicted_price: float = Field(..., description="Preço previsto do livro")
