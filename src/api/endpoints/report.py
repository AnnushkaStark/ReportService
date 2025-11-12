from typing import Literal

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from fastapi import status
from fastapi_filter import FilterDepends

from api.depends.table_report import get_table_report_by_id
from api.depends.table_report import get_table_report_service
from api.depends.template import get_template_id
from api.depends.user import get_user_id
from api.filters.table_report import TableReportFilter
from models import TableReport
from schemas import PaginationResponse
from schemas.report_table import TableReportResponse
from services.table_report import TableReportService
from utils.errors import ErrorCodes
from utils.errors import errs
from utils.types import Ok

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses=errs(
        e422=[ErrorCodes.FILE_IS_EMPTY, ErrorCodes.INVALID_FILE_FORMAT, ErrorCodes.NOT_ALL_COILUMS_HAS_UNIQUE_NAMES]
    ),
)
async def create_report(
    file: UploadFile = File(...),
    user_id: int = Depends(get_user_id),
    template_id: int = Depends(get_template_id),
    additional_params: str = Form(default=None),
    service: TableReportService = Depends(get_table_report_service),
) -> Ok:
    return await service.create(
        file=file, uer_id=user_id, template_id=template_id, additional_params={"additional_params": additional_params}
    )


@router.get(
    "/{report_id}/metadata",
    response_model=TableReportResponse,
    responses=(_report_not_found_err := (errs(e404=ErrorCodes.REPORT_NOT_FOUND))),
)
async def read_report_metadata(found_report: TableReport = Depends(get_table_report_by_id)):
    return found_report


@router.get("/full_data/{report_id}/", response_model=None, responses=_report_not_found_err)
async def get_report_data(
    report_id: int,
    mode: Literal["json", "excel"],
    service: TableReportService = Depends(get_table_report_service),
    user_id: int = Depends(get_user_id),
):
    return await service.get_table_report_full_data(obj_id=report_id, mode=mode, user_id=user_id)


@router.get("/", response_model=PaginationResponse[TableReportResponse])
async def read_table_reports(
    limit: int = 20,
    offset: int = 0,
    filter: TableReportFilter = FilterDepends(TableReportFilter),
    user_id: int = Depends(get_user_id),
):
    return await filter.filter(user_id=user_id, offset=offset, limit=limit)
