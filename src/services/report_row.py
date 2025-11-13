from typing import List

from repositories.report_row import ReportRowRepository
from schemas import StatsRow
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

    async def _create_row_values(self, keys: List[str], values: List[str], row_ids: List[int]) -> None:
        await self.report_value_service.create_multi(values=values, columns=keys, rows_ids=row_ids)

    async def get_stats_schema(self, report_id: int, rows_ids: List[int]) -> StatsRow:
        return StatsRow(
            report_id=report_id,
            not_null_values=await self.repository.get_unique_row_count_by_report_id(report_id=report_id),
            null_values=await self.repository.get_nullable_row_count_by_report_id(report_id=report_id),
            deleted_values=await self.repository.get_deleted_row_count_by_report_id(report_id=report_id),
            updated_values=await self.repository.get_updated_row_count_by_report_id(report_id=report_id),
            value_stats=await self.report_value_service.get_list_schemas(rows_ids=rows_ids),
        )
