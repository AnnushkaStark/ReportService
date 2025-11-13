from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReportRow

from .base import AbstactBaseRepository


class ReportRowRepository(AbstactBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TableReportRow)

    async def get_unique_row_count_by_report_id(self, report_id: int) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(
                self.model.unique_value.isnot(None), self.model.report_id == report_id
            )
        )
        return statement.scalar()

    async def get_nullable_row_count_by_report_id(self, report_id: int) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(
                self.model.unique_value.is_(None), self.model.report_id == report_id
            )
        )
        return statement.scalar()

    async def get_updated_row_count_by_report_id(self, report_id: int) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(
                self.model.updated_at.isnot(None), self.model.report_id == report_id
            )
        )
        return statement.scalar()

    async def get_deleted_row_count_by_report_id(self, report_id: int) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.is_deleted.is_(True), self.model.report_id == report_id)
        )
        return statement.scalar()
