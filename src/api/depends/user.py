from depends.database import get_async_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from services.user import UserService


async def get_user_repository(session: AsyncSession = Depends(get_async_db)) -> UserRepository:
    return UserRepository(session=session)


async def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repository)


async def get_user_id(service: UserService = Depends(get_user_service)) -> int:
    user = await service.get_or_create()
    return user.id
