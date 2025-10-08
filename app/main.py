from fastapi import FastAPI

from app.core.database import init_db
from app.core.routers import register_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Tech Challenge 01",
        description="Aplicação do módulo 1",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )

    register_routers(app)

    init_db(app)

    return app


app = create_app()
