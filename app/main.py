from fastapi import  FastAPI
from .controllers import health_check

app = FastAPI(title="Tech Challenge 01", version="0.1.0")

app.include_router(health_check.router, tags=["health"])