from fastapi import APIRouter, Depends

from app.dtos.category_stats import CategoryStatsDto
from app.dtos.general_stats import GeneralStatsDto
from app.services.book_service import BookService
from app.services.category_service import CategoryService

router = APIRouter(prefix="/stats")


@router.get(
    "/overview", description="Estatísticas gerais da coleção", response_model=GeneralStatsDto
)
async def get_geral_insights(bookService: BookService = Depends()):
    return await bookService.get_overview_stats()


@router.get(
    "/categories",
    description="Estatísticas detalhada por categoria",
    response_model=list[CategoryStatsDto],
)
async def get_category_insights(categoryService: CategoryService = Depends()):
    return await categoryService.get_categories_stats()
