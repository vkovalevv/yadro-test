from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.external import RandomDataClient


async def load_users(
    session: AsyncSession,
    client: RandomDataClient,
    count: int
) -> int:
    external_users = await client.fetch_users(count)
    if not external_users:
        return 0

    await session.execute(
        insert(User),
        [user.model_dump() for user in external_users]
    )
    await session.commit()
    return len(external_users)
