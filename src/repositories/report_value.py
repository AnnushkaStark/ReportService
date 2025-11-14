from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReportValue

from .base import AbstactBaseRepository


class ReportValueRepository(AbstactBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TableReportValue)

    async def get_total_value_count_by_rows_ids(self, rows_ids: List[int]) -> int:
        statement = await self.session.execute(select(func.count(self.model.id)).where(self.model.row_id.in_(rows_ids)))
        return statement.scalar()

    async def get_unique_value_count_by_rows_ids(self, rows_ids: List[int]) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.value.isnot(None), self.model.row_id.in_(rows_ids))
        )
        return statement.scalar()

    async def get_nullable_value_count_by_rows_ids(self, rows_ids: List[int]) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.value.is_(None), self.model.row_id.in_(rows_ids))
        )
        return statement.scalar()

    async def get_updated_value_count_by_rows_ids(self, rows_ids: List[int]) -> int:
        statement = await self.session.execute(
            select(func.count(self.model.id)).where(self.model.updated_at.isnot(None), self.model.row_id.in_(rows_ids))
        )
        return statement.scalar()

    async def mark_updated_by_rows_ids(self, rows_ids: List[int]) -> None:
        await self.session.execute(
            update(self.model).values(updated_at=datetime.now(tz=None)).where(self.model.row_id.in_(rows_ids))
        )
        await self.session.commit()
