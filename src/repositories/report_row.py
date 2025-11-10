from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReportRow

from .base import AbstactBaseRepository


class ReportRowRepository(AbstactBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TableReportRow)
