import os
from collections.abc import AsyncIterator

from app.db.models import User

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.db.base import Base
from app.db.session import get_session
from app.main import create_app

TEST_DATABASE_URL = os.getenv(
    'TEST_DATABASE_URL',
    'postgresql+asyncpg://app:app@localhost:5433/app_test'
)


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine) -> AsyncIterator[AsyncSession]:
    session_local = async_sessionmaker(engine, expire_on_commit=False)
    async with session_local() as session:
        yield session


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncIterator[AsyncClient]:
    app = create_app(lifespan=None)

    async def override_get_session() -> AsyncIterator[AsyncSession]:
        yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client


@pytest_asyncio.fixture
async def seeded_users(session: AsyncSession) -> list[User]:
    users = [
        User(
            first_name=f'User{i}',
            last_name=f'Test',
            gender='Мужчина' if i % 2 == 0 else 'Женщина',
            phone=f'+7 (999) 000-00-{i:02d}',
            email=f'user{i}@test.com',
            address=f'Address {i}'
        )
        for i in range(5)
    ]
    session.add_all(users)
    await session.commit()
    return users
