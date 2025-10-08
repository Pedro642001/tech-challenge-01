from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class User(Model):
    id = fields.IntField(primary_key=True, generated=True)

    name = fields.CharField(max_length=255)

    email = fields.CharField(max_length=255, unique=True)

    password_hash = fields.CharField(max_length=255)

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"
        indexes = ["email", "name", "password_hash"]


get_user_dto = pydantic_model_creator(
    User,
    name="User",
    model_config={"extra": "ignore"},
    exclude=("password_hash"),
    include=("id", "name", "email"),
)

create_user_dto = pydantic_model_creator(
    User,
    name="CreateUser",
    model_config={"extra": "ignore"},
    exclude=("id", "password_hash"),
)
