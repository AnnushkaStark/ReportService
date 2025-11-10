from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReport

from .base import AbstactBaseRepository


class TableReportRepository(AbstactBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TableReport)
