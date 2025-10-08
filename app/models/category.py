from __future__ import annotations

from datetime import datetime

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Category(Model):
    id: int = fields.IntField(primary_key=True, generated=True)

    name: str = fields.CharField(max_length=255, unique=True, null=False)

    link: str = fields.CharField(max_length=255, null=False)

    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    updated_at: datetime = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "categories"
        indexes = ["name"]


get_category_dto = pydantic_model_creator(
    Category, name="Category", model_config={"extra": "allow"}
)
