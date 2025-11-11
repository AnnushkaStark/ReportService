from typing import List

from models import TableReportRow
from repositories.report_row import ReportRowRepository
from schemas.report_row import ReportRowCreateDB
from services.report_value import ReportValueService
from utils.errors import DomainError
from utils.errors import ErrorCodes


class ReportRowService:
    def __init__(self, repository: ReportRowRepository, report_value_service: ReportValueService):
        self.repository = repository
        self.report_value_service = report_value_service

    async def _check_unique(self, metadata: List[str]) -> None:
        if not len(metadata) == len(set(metadata)):
            raise DomainError(ErrorCodes.NOT_ALL_COILUMS_HAS_UNIQUE_NAMES)

    async def _get_schema_multi(self, values: List[str], report_id: int) -> List[ReportRowCreateDB]:
        return [ReportRowCreateDB(unique_value=value, report_id=report_id) for value in values]

    async def create_rows_multi(self, report_id: int, values: List[str]) -> List[int]:
        rows = await self.repository.create_bulk(
            schemas=await self._get_schema_multi(values=values, report_id=report_id)
        )
        return [row.id for row in rows]

    async def _create_row_values(self, df_dict: dict, row_ids: List[int]) -> None:
        zipped_list = list(zip(df_dict, row_ids, strict=True))
        await self.report_value_service.create_multi(values=zipped_list)
