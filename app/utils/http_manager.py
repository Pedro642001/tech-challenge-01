import httpx
from bs4 import BeautifulSoup


class HttpManager:
    @staticmethod
    def get_session() -> httpx.AsyncClient:
        return httpx.AsyncClient(
            headers={"User-Agent": "Mozilla/5.0 (compatible; BookScraperBot/1.0)"},
            limits=httpx.Limits(max_connections=10),
            timeout=50,
        )

    @staticmethod
    def format_book_url(url: str, path: str) -> str:
        return f"{url}catalogue/{path}"

    @staticmethod
    async def get_response_html(
        url: str, session: httpx.AsyncClient | None = None
    ) -> BeautifulSoup:
        if session:
            response = await session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        else:
            async with httpx.AsyncClient() as temp_session:
                response = await temp_session.get(url)
                response.raise_for_status()
                return BeautifulSoup(response.text, "html.parser")
