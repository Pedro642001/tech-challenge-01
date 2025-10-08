from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.settings import settings


def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
