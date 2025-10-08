from fastapi import APIRouter, Depends

from app.models.category import get_category_dto
from app.services.category_service import CategoryService
from app.utils.filter import Filter

router = APIRouter(prefix="/categories")


@router.get(
    "/", description="Lista todas as categorias de livros", response_model=list[get_category_dto]
)
async def get_categories(categoryService: CategoryService = Depends(), filter: Filter = Depends()):
    return await get_category_dto.from_queryset(categoryService.get_all_categories(filter))
