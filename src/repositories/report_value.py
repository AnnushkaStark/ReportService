from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReportValue

from .base import AbstactBaseRepository


class ReportValueRepository(AbstactBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TableReportValue)
