from typing import Optional

from fastapi import APIRouter, Query
from fastapi.params import Depends

from app.models.book import get_book_dto
from app.services.book_service import BookService
from app.utils.filter import Filter

router = APIRouter(prefix="/books")


@router.get("/", description="Lista todos os livros disponíveis", response_model=list[get_book_dto])
async def get_books(
    bookService: BookService = Depends(),
    filter: Filter = Depends(),
):
    return await get_book_dto.from_queryset(bookService.get_all_books(filter))


@router.get("/search", description="Busca filtrada por livros", response_model=list[get_book_dto])
async def search_book(
    bookService: BookService = Depends(),
    filter: Filter = Depends(),
    category_name: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
):
    filter.query_by.setdefault("title__icontains", title) if title else None
    filter.query_by.setdefault(
        "category__name__icontains", category_name
    ) if category_name else None

    return await get_book_dto.from_queryset(bookService.get_by_filter(filter))


@router.get(
    "/price-range",
    description="Lista os livros dentro de uma faixa de preço",
    response_model=list[get_book_dto],
)
async def get_books_price_range(
    min_price: float = Query(1, description="Preço mínimo dos livros", ge=1, le=1000),
    max_price: float = Query(55.32, description="Preço máximo dos livros", ge=1, le=1000),
    filter: Filter = Depends(),
    bookService: BookService = Depends(),
):
    return await get_book_dto.from_queryset(
        bookService.get_by_price_and_filter(min_price, max_price, filter)
    )


@router.get(
    "/top-rated",
    description="Lista os 10 livros mais bem avaliados",
    response_model=list[get_book_dto],
)
async def get_books_insights(bookService: BookService = Depends()):
    return await get_book_dto.from_queryset(bookService.get_top_rated_books())


@router.get("/{id}", description="Busca livro por ID", response_model=get_book_dto)
async def get_book(id: int, bookService: BookService = Depends()):
    return await get_book_dto.from_queryset_single(bookService.get_by_id(id))
