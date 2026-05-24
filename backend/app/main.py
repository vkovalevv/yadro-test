import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import Lifespan

from app.api import users
from app.config import get_settings
from app.db.session import AsyncSessionLocal
from app.external import get_random_data_client
from app.services.users import load_users

logger = logging.getLogger(__name__)


@asynccontextmanager
async def default_lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    client = get_random_data_client()

    async with AsyncSessionLocal() as session:
        inserted = await load_users(session, client, settings.initial_load_count)
    logger.info('Loaded %d users from external API', inserted)

    yield


def create_app(lifespan: Lifespan[FastAPI] | None = default_lifespan) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:5173','http://localhost:3000'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
    app.include_router(users.router)
    return app


app = create_app()
