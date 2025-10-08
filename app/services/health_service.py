from tortoise import Tortoise


class HealthService:
    async def check_health(self) -> bool:
        return await self._check_database_connection()

    async def _check_database_connection(self):
        try:
            await Tortoise.get_connection("default").execute_query("SELECT 1")
            return True
        except Exception:
            return False
