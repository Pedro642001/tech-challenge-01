from fastapi import FastAPI

from app.controllers import (
    auth,
    books,
    categories,
    health_check,
    insights,
    machine_learning,
    users,
    web_scrapping,
)
from app.core.settings import settings


def register_routers(app: FastAPI):
    prefix = settings.API_PREFIX

    app.include_router(health_check.router, tags=["Health Check"], prefix=prefix)
    app.include_router(auth.router, tags=["Auth"], prefix=prefix)
    app.include_router(web_scrapping.router, tags=["Web Scraping"], prefix=prefix)
    app.include_router(books.router, tags=["Books"], prefix=prefix)
    app.include_router(categories.router, tags=["Categories"], prefix=prefix)
    app.include_router(users.router, tags=["Users"], prefix=prefix)
    app.include_router(insights.router, tags=["Insights"], prefix=prefix)
    app.include_router(machine_learning.router, tags=["Machine Learning"], prefix=prefix)
