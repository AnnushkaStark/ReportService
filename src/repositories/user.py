from sqlalchemy.ext.asyncio import AsyncSession

from models import User

from .base import AbstactBaseRepository


class UserRepository(AbstactBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
