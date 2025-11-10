from fastapi import UploadFile

from models import TableReport
from repositories.report_table import TableReportRepository
from schemas.report_table import TableReportBase
from services.report_row import ReportRowService
from utils.exel_parser import ExcelParser


class TableReportService:
    def __init__(self, repository: TableReportRepository, report_row_service: ReportRowService):
        self.repository = repository
        self.report_row_service = report_row_service

    async def _get_schema(
        self, file: UploadFile, uer_id: int, template_id: int, additional_params: dict
    ) -> TableReportBase:
        parser = ExcelParser(file=file)
        df = await parser.read_excel()
        return TableReportBase(
            user_id=uer_id,
            template_id=template_id,
            columns_metadata=await parser.extract_metadata(df=df),
            total_rows=await parser.get_total_rows_count(df=df),
            additional_params=additional_params,
        )

    async def create(self, file: UploadFile, uer_id: int, template_id: int, additional_params: dict) -> TableReport:
        await self.repository.create(
            schema=await self._get_schema(
                file=file, uer_id=uer_id, template_id=template_id, additional_params=additional_params
            )
        )
