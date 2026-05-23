from typing import Any

import httpx

from app.config import get_settings
from .schemas import ExternalUser


class RandomDataClient:
    MAX_PER_REQUEST = 100

    def __init__(self, base_url: str, timeout: float = 30.0):
        self._base_url = base_url
        self._timeout = timeout

    async def fetch_users(self, count: int) -> list[ExternalUser]:
        results: list[ExternalUser] = []
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            while len(results) < count:
                batch_size = min(self.MAX_PER_REQUEST,
                                 count - len(results))
                response = await client.get(self._base_url, params={'count': batch_size})
                response.raise_for_status()
                payload: Any = response.json()

                if isinstance(payload, dict):
                    payload = [payload]

                results.extend(ExternalUser.model_validate(item)
                               for item in payload)

        return results


def get_random_data_client() -> RandomDataClient:
    return RandomDataClient(base_url=get_settings().external_api_url)
