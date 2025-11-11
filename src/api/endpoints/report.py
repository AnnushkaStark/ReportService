from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from fastapi import status

from api.depends.table_report import get_table_report_service
from api.depends.template import get_template_id
from api.depends.user import get_user_id
from services.table_report import TableReportService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_report(
    file: UploadFile = File(...),
    user_id: int = Depends(get_user_id),
    template_id: int = Depends(get_template_id),
    additional_params: str = Form(default=None),
    service: TableReportService = Depends(get_table_report_service),
) -> None:
    await service.create(
        file=file, uer_id=user_id, template_id=template_id, additional_params={"additional_params": additional_params}
    )
