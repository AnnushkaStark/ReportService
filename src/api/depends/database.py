from sqlalchemy.ext.asyncio import AsyncSession

from database.databases import async_session


async def get_async_db() -> AsyncSession:
    async with async_session() as session:
        yield session
