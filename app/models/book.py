from datetime import datetime

from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from app.models.category import Category


class Book(Model):
    id: int = fields.IntField(primary_key=True, generated=True)

    title: str = fields.CharField(max_length=255)

    description: str = fields.CharField(max_length=10000)

    url: str = fields.CharField(max_length=255)

    image_url: str = fields.CharField(max_length=255)

    price: float = fields.DecimalField(max_digits=10, decimal_places=2)

    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        "models.Category",
        related_name="books",
        on_delete=fields.CASCADE,
    )

    rating: int = fields.IntField()

    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    updated_at: datetime = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "books"
        unique_together = ("title", "url")
        indexes = ["title", "rating", "price"]


Tortoise.init_models(["app.models.book", "app.models.category"], "models")

get_book_dto = pydantic_model_creator(Book, name="Book")
