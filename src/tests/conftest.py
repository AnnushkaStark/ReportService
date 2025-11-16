import sys
from typing import Generator

import pytest_asyncio
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database.databases import Base
from database.databases import async_engine
from main import app

from .fixtures import *  # noqa: F403, F401

assert (sys.version_info.major, sys.version_info.minor) == (
    3,
    12,
), "Only Python 3.11 allowed"


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture
async def http_client(
    async_session: AsyncSession,
) -> Generator[AsyncClient, None, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://0.0.0.0:8000") as ac:
        yield ac
