from datetime import date
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import func
from sqlalchemy import select

from database.databases import get_async_session
from models import TableReport
from schemas import PaginationResponse
from schemas.report_table import TableReportResponse


class TableReportFilter(Filter):
    created_at__gte: Optional[date] = None
    created_at__lte: Optional[date] = None
    updated_at__gte: Optional[date] = None
    updated_at__lte: Optional[date] = None
    total_rows__gte: Optional[int] = None
    total_rows__lte: Optional[int] = None

    class Constants(Filter.Constants):
        model = TableReport

    async def filer(self, user_id: int, limit: int = 20, offset: int = 0) -> PaginationResponse[TableReportResponse]:
        async for session in get_async_session():
            statement = (
                select(self.Constants.model, func.count().over().label("total"))
                .where(self.Constants.model.user_id == user_id)
                .limit(limit)
                .offset(offset)
            )
            if self.created_at__gte is not None:
                statement = statement.where(func.date(self.Constants.model.created_at) >= self.created_at__gte)
            if self.created_at__lte is not None:
                statement = statement.where(func.date(self.Constants.model.created_at) <= self.created_at__lte)
            if self.updated_at__gte is not None:
                statement = statement.where(func.date(self.Constants.model.updated_at) >= self.updated_at__gte)
            if self.updated_at__lte is not None:
                statement = statement.where(func.date(self.Constants.model.updated_at) <= self.updated_at__lte)
            if self.total_rows__gte is not None:
                statement = statement.where(self.Constants.model.total_rows >= self.total_rows__gte)
            if self.total_rows__lte is not None:
                statement = statement.where(self.Constants.model.total_rows <= self.total_rows__gte)
            result = await session.execute(statement)
            rows = result.mappings().all()
            return PaginationResponse.create(
                limit=limit,
                offset=offset,
                count=rows[0]["total"] if rows else 0,
                items=[r["TableReport"] for r in rows],
            )
