from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReportValue

from .base import AbstactBaseRepository


class ReportValueRepository(AbstactBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TableReportValue)

    async def get_total_value_count_by_row_id(self, row_id: int) -> int:
        statement = await self.session.execute(select(func.count(self.model.id)).where(self.model.row_id == row_id))
        return statement.scalar()

    async def get_unique_value_count_by_row_id(self, row_id: int) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.value.isnot(None), self.model.row_id == row_id)
        )
        return statement.scalar()

    async def get_nullable_value_count_by_row_id(self, row_id: int) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.value.is_(None), self.model.row_id == row_id)
        )
        return statement.scalar()

    async def get_updated_value_count_by_row_id(self, row_id: int) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.updated_at.isnot(None), self.model.row_id == row_id)
        )
        return statement.scalar()
