import asyncio
from typing import Any

import httpx

from app.config import get_settings
from .schemas import ExternalUser


class RandomDataClient:
    MAX_PER_REQUEST = 100
    MAX_CONCURRENCY = 5

    def __init__(self, base_url: str, timeout: float = 30.0):
        self._base_url = base_url
        self._timeout = timeout

    async def fetch_users(self, count: int) -> list[ExternalUser]:
        if count <= 0:
            return []

        batch_sizes = self._split_into_batches(count)
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENCY)

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            tasks = [self._fetch_batch(client, size, semaphore)
                     for size in batch_sizes]
            batches = await asyncio.gather(*tasks)

        results = [user for batch in batches for user in batch]
        return results[:count]

    def _split_into_batches(self, count: int) -> list[int]:
        full, remainder = divmod(count, self.MAX_PER_REQUEST)
        sizes = [self.MAX_PER_REQUEST] * full
        if remainder:
            sizes.append(remainder)
        return sizes

    async def _fetch_batch(
        self,
        client: httpx.AsyncClient,
        size: int,
        semaphore: asyncio.Semaphore,
    ) -> list[ExternalUser]:
        async with semaphore:
            response = await client.get(self._base_url, params={"count": size})
            response.raise_for_status()
            payload: Any = response.json()

        if isinstance(payload, dict):
            payload = [payload]

        return [ExternalUser.model_validate(item) for item in payload]


def get_random_data_client() -> RandomDataClient:
    return RandomDataClient(base_url=get_settings().external_api_url)
