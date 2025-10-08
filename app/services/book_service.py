from http.client import HTTPException

from tortoise.functions import Avg
from tortoise.queryset import QuerySet

from app.models.book import Book
from app.utils.filter import Filter


class BookService:
    async def bulk_create_books(self, books: list[Book]) -> list[Book]:
        return await Book.bulk_create(
            books,
            ignore_conflicts=True,
            batch_size=100,
        )

    async def create(self, book: Book) -> Book:
        return await Book.create(book)

    def get_by_id(self, id: int) -> Book:
        return Book.get(id=id)

    def get_by_filter(self, filter: Filter) -> QuerySet[Book]:
        return (
            Book.filter(**filter.query_by)
            .order_by(filter.order_by)
            .offset(filter.offset)
            .limit(filter.limit)
        )

    def get_all_books(self, filters: Filter) -> QuerySet[Book]:
        return Book.all().order_by(filters.order_by).offset(filters.offset).limit(filters.limit)

    def get_top_rated_books(self) -> QuerySet[Book]:
        return Book.all().order_by("-rating").limit(10)

    def get_by_price_and_filter(
        self, min_price: float, max_price: float, filter: Filter
    ) -> QuerySet[Book]:
        if min_price > max_price:
            raise HTTPException(
                detail="O preço mínimo não pode ser maior que o preço máximo", status_code=400
            )

        filter.query_by["price__gte"] = min_price
        filter.query_by["price__lte"] = max_price

        return self.get_by_filter(filter)

    async def get_overview_stats(self) -> QuerySet[Book]:
        total_books = await Book.all().count()
        average_price = await Book.all().annotate(avg=Avg("price")).values_list("avg", flat=True)
        average_price = float(average_price[0]) if average_price else 0.0

        rating_buckets = [
            {"range": "0-1", "count": await Book.filter(rating__gte=0, rating__lt=1).count()},
            {"range": "1-2", "count": await Book.filter(rating__gte=1, rating__lt=2).count()},
            {"range": "2-3", "count": await Book.filter(rating__gte=2, rating__lt=3).count()},
            {"range": "3-4", "count": await Book.filter(rating__gte=3, rating__lt=4).count()},
            {"range": "4-5", "count": await Book.filter(rating__gte=4, rating__lte=5).count()},
        ]

        return {
            "total_books": total_books,
            "average_price": average_price,
            "rating_distribution": rating_buckets,
        }
