from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app.models.user import User
from app.services.auth_service import AuthService
from app.services.book_service import BookService
from app.services.category_service import CategoryService
from app.services.web_scraping import WebScrapingService

router = APIRouter()


@router.post(
    "/trigger",
    description="Realiza varredura por novos livros",
    response_description="Mensagem de sucesso",
    responses={
        200: {"description": "Web scraping finalizado com sucesso!"},
        401: {"description": "Não autorizado"},
    },
)
async def scraping(
    current_user: Annotated[User, Depends(AuthService.get_current_user)],
    webScrapingService: Annotated[
        WebScrapingService, Depends(lambda: WebScrapingService(CategoryService(), BookService()))
    ],
):
    await webScrapingService.run()
    return {"message": "execução do web scraping finalizada com sucesso!"}
