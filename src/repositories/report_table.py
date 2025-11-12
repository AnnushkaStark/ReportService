from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

from models import TableReport
from models import TableReportRow

from .base import AbstactBaseRepository


class TableReportRepository(AbstactBaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TableReport)

    async def get_by_id_and_user_id(self, obj_id: int, user_id: int) -> Optional[TableReport]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id, self.model.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_full_by_id_and_user_id(self, user_id: int, obj_id: int) -> Optional[TableReport]:
        statement = (
            select(self.model)
            .where(self.model.user_id == user_id, self.model.id == obj_id)
            .options(selectinload(self.model.rows).selectinload(TableReportRow.values))
        )
        retsult = await self.session.execute(statement)
        return retsult.scalars().unique().first()

    async def get_with_row_ids(self, report_id: int, user_id: int) -> Optional[TableReport]:
        statement = await self.session.execute(
            select(self.model)
            .where(self.model.id == report_id, self.model.user_id == user_id)
            .options(joinedload(self.model.rows).load_only("id"))
        )
        return statement.unique().scalar_one_or_none()
