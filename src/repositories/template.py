from sqlalchemy.ext.asyncio import AsyncSession

from models import Template

from .base import AbstactBaseRepository


class TempltateRepository(AbstactBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Template)
