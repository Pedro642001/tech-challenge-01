from typing import List

from tortoise.functions import Avg, Count, Max, Min
from tortoise.queryset import QuerySet

from app.dtos.category_insigth import CategoryInsightDto
from app.models.category import Category
from app.utils.filter import Filter


class CategoryService:
    async def bulk_create_categories(self, categories: List[Category]) -> List[Category]:
        return await Category.bulk_create(
            categories,
            ignore_conflicts=True,
            batch_size=50,
        )

    def get_all_categories(self, filter: Filter) -> QuerySet[Category]:
        return Category.all().order_by(filter.order_by).offset(filter.offset).limit(filter.limit)

    async def get_categories_stats(self) -> List[CategoryInsightDto]:
        stats = await Category.annotate(
            total_books=Count("books"),
            average_price=Avg("books__price"),
            min_price=Min("books__price"),
            max_price=Max("books__price"),
        ).values("name", "total_books", "average_price", "min_price", "max_price")

        return [
            CategoryInsightDto(
                name=s["name"],
                total_books=s["total_books"],
                average_price=float(s["average_price"] or 0),
                min_price=float(s["min_price"] or 0),
                max_price=float(s["max_price"] or 0),
            )
            for s in stats
        ]
