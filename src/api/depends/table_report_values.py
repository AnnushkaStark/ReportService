from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends.database import get_async_db
from repositories.report_value import ReportValueRepository
from services.report_value import ReportValueService


async def get_report_values_repository(session: AsyncSession = Depends(get_async_db)) -> ReportValueRepository:
    return ReportValueRepository(session=session)


async def get_report_value_service(repository: ReportValueRepository) -> ReportValueService:
    return ReportValueService(repository=repository)
