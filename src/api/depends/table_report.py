from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends.database import get_async_db
from api.depends.table_report_rows import get_report_row_service
from api.depends.user import get_user_id
from repositories.report_table import TableReportRepository
from services.report_row import ReportRowService
from services.table_report import TableReportService
from utils.errors import ErrorCodes


async def get_table_report_repository(session: AsyncSession = Depends(get_async_db)) -> TableReportRepository:
    return TableReportRepository(session=session)


async def get_table_report_service(
    repository: TableReportRepository = Depends(get_table_report_repository),
    report_row_service: ReportRowService = Depends(get_report_row_service),
) -> TableReportService:
    return TableReportService(repository=repository, report_row_service=report_row_service)


async def get_table_report_by_id(
    report_id: int, service: TableReportService = Depends(get_table_report_service), user_id: int = Depends(get_user_id)
):
    if found_report := await service.get_report_metadata(obj_id=report_id, user_id=user_id):
        return found_report
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCodes.REPORT_NOT_FOUND.value)
