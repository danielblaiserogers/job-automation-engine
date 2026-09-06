import httpx
from app.core.config import settings

class AdzunaClient:
    BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    @classmethod
    async def fetch_jobs(cls, query: str = "python developer", location: str = "remote", results_per_page: int = 10) -> list[dict]:
        params = {
            "app_id": settings.ADZUNA_APP_ID,
            "app_key": settings.ADZUNA_APP_KEY,
            "results_per_page": results_per_page,
            "what": query,
            "where": location,
            "content-type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])