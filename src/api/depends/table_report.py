from depends.database import get_async_db
from depends.table_report_rows import get_report_row_service
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.report_table import TableReportRepository
from services.report_row import ReportRowService
from services.table_report import TableReportService


async def get_table_report_repository(session: AsyncSession = Depends(get_async_db)) -> TableReportRepository:
    return TableReportRepository(session=session)


async def get_table_report_service(
    repository: TableReportRepository = Depends(get_table_report_repository),
    report_row_service: ReportRowService = Depends(get_report_row_service),
) -> TableReportService:
    return TableReportService(repository=repository, report_row_service=report_row_service)
