import asyncio
import re

from bs4 import BeautifulSoup
from httpx import AsyncClient

from app.core.settings import settings
from app.models.book import Book
from app.models.category import Category
from app.services.book_service import BookService
from app.services.category_service import CategoryService
from app.utils.http_manager import HttpManager


class WebScrapingService:
    def __init__(
        self,
        categoryService: CategoryService,
        bookService: BookService,
    ):
        self.categoryService = categoryService

        self.bookService = bookService

        self.base_url = settings.URL_TO_SCRAP

        self._book_parser = _BookParser(self.base_url)

    async def run(self) -> list[Category]:
        async with HttpManager.get_session() as session:
            base_html = await HttpManager.get_response_html(self.base_url, session)

            await self._register_categories_from_html(base_html)

            total_pages = self._get_total_pages(base_html)

            page_urls = [self._get_page_url_formatted(page) for page in range(1, total_pages + 1)]

            await asyncio.gather(*(self.process_page(url, session) for url in page_urls))

    async def process_page(self, page_url: str, session: AsyncClient):
        page_html = await HttpManager.get_response_html(page_url, session)

        await self._register_books_from_html(page_html, session)

    async def _register_categories_from_html(self, html: BeautifulSoup):
        ul = html.find("ul", class_="nav nav-list")

        category_links = [a for a in ul.find_all("a") if a.get_text(strip=True) != "Books"]

        semaphore = asyncio.Semaphore(30)

        async def process_category(html_element: BeautifulSoup) -> Category:
            async with semaphore:
                return Category(
                    name=html_element.get_text(strip=True),
                    link=self.base_url + html_element["href"],
                )

        categories = await asyncio.gather(
            *(process_category(html_element) for html_element in category_links)
        )

        await self.categoryService.bulk_create_categories(categories)

    async def _register_books_from_html(self, html: BeautifulSoup, session: AsyncClient):
        book_urls = self._get_book_urls(html)

        max_concurrent_requests = 50

        semaphore = asyncio.Semaphore(max_concurrent_requests)

        books: list[Book] = []

        async def process_book(url: str) -> Book:
            async with semaphore:
                book_html = await HttpManager.get_response_html(url, session=session)

                return Book(
                    title=self._book_parser._get_title(book_html),
                    price=self._book_parser._get_price(book_html),
                    stock=self._book_parser._get_stock(book_html),
                    url=url,
                    description=self._book_parser._get_description(book_html),
                    category_id=await self._book_parser._get_category(book_html),
                    rating=self._book_parser._get_rating(book_html),
                    image_url=self._book_parser._get_image_url(book_html),
                )

        chunk_size = max_concurrent_requests

        for index in range(0, len(book_urls), chunk_size):
            chunk = book_urls[index : index + chunk_size]

            books = await asyncio.gather(*(process_book(url) for url in chunk))

            await self.bookService.bulk_create_books(books)

            with open("scraped_books.log", "a") as log_file:
                for book in books:
                    log_file.write(f"{book.title}-{book.url}\n")

    def _get_book_urls(self, html: BeautifulSoup) -> list[str]:
        articles = html.find_all("article", class_="product_pod")
        return [HttpManager.format_book_url(self.base_url, a.h3.a["href"]) for a in articles]

    def _get_total_pages(self, html: BeautifulSoup):
        text_in_li = html.find("li", class_="current").get_text(strip=True).split(" ")
        total_pages = int(text_in_li[-1])
        return total_pages

    def _get_page_url_formatted(self, page: int) -> str:
        return f"{self.base_url}catalogue/page-{page}.html"


class _BookParser:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def parse_book(self, html: BeautifulSoup, url: str) -> Book:
        return Book(
            title=self._get_title(html),
            price=self._get_price(html),
            stock=self._get_stock(html),
            url=url,
            description=self._get_description(html),
            category=self._get_category(html),
            rating=self._get_rating(html),
            image_url=self._get_image_url(html),
        )

    def _get_title(self, html: BeautifulSoup) -> str:
        return html.find("h1").get_text(strip=True)

    def _get_price(self, html: BeautifulSoup) -> float:
        return float(html.find("p", class_="price_color").get_text(strip=True).replace("£", ""))

    def _get_stock(self, html: BeautifulSoup) -> int:
        text = html.find("p", class_="instock availability").get_text(strip=True)
        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0

    def _get_description(self, html: BeautifulSoup) -> str:
        return html.find("meta", attrs={"name": "description"})["content"].strip()

    async def _get_category(self, html: BeautifulSoup) -> int:
        return (
            await Category.get(
                name=html.find("ul", class_="breadcrumb").find_all("li")[2].a.get_text(strip=True)
            )
        ).id

    def _get_rating(self, html: BeautifulSoup) -> int:
        rating = html.find("p", class_="star-rating")["class"][1]
        mapping = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        return mapping.get(rating, 0)

    def _get_image_url(self, html: BeautifulSoup) -> str:
        src = html.find("div", class_="item active").img["src"]
        return self.base_url + src.replace("../../", "")
