from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends.database import get_async_db
from api.depends.table_report_values import get_report_value_service
from repositories.report_row import ReportRowRepository
from services.report_row import ReportRowService
from services.report_value import ReportValueService


async def get_report_row_repository(session: AsyncSession = Depends(get_async_db)) -> ReportRowRepository:
    return ReportRowRepository(session=session)


async def get_report_row_service(
    repository: ReportRowRepository = Depends(get_report_row_repository),
    report_value_service: ReportValueService = Depends(get_report_value_service),
) -> ReportRowService:
    return ReportRowService(repository=repository, report_value_service=report_value_service)
