from typing import List
from typing import Literal

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

    async def _check_unique(self, values: List[str]) -> None:
        if len(values) != len(set(values)):
            raise DomainError(ErrorCodes.NOT_ALL_COILUMS_HAS_UNIQUE_NAMES)

    async def _get_schema_multi(self, values: List[str], report_id: int) -> List[ReportRowCreateDB]:
        await self._check_unique(values=values)
        return [ReportRowCreateDB(unique_value=value, report_id=report_id) for value in values]

    async def create_rows_multi(self, report_id: int, values: List[str]) -> List[int]:
        rows = await self.repository.create_bulk(
            schemas=await self._get_schema_multi(values=values, report_id=report_id)
        )
        return rows

    async def _create_row_values(self, keys: List[str], values: List[str], rows_ids: List[int]) -> None:
        await self.report_value_service.create_multi(values=values, columns=keys, rows_ids=rows_ids)

    async def get_stats_schema(self, report_id: int, rows_ids: List[int]) -> StatsRow:
        return StatsRow(
            report_id=report_id,
            not_null_values=await self.repository.get_unique_row_count_by_report_id(report_id=report_id),
            null_values=await self.repository.get_nullable_row_count_by_report_id(report_id=report_id),
            deleted_values=await self.repository.get_deleted_row_count_by_report_id(report_id=report_id),
            updated_values=await self.repository.get_updated_row_count_by_report_id(report_id=report_id),
            value_stats=await self.report_value_service.get_stat_schema(rows_ids),
        )

    async def _append(self, values: List[str], old_rows_ids: List[int], keys: List[str]) -> List[int]:
        return await self._create_row_values(values=values, rows_ids=old_rows_ids, keys=keys)

    async def _replace(self, values: List[str], report_id: int, keys: List[str]) -> List[int]:
        await self.repository.mark_deleted_by_report_id(report_id=report_id)
        rows = await self.create_rows_multi(report_id=report_id, values=keys)
        await self._create_row_values(
            values=values, keys=[row.unique_value for row in rows], rows_ids=[row.id for row in rows]
        )

    async def update(
        self,
        keys: List[str],
        report_id: int,
        values: List[str],
        mode: Literal["append", "replace"],
        old_rows_ids: List[int],
    ) -> None:
        match mode:
            case "append":
                await self._append(values=values, old_rows_ids=old_rows_ids, keys=keys)
            case "replace":
                await self._replace(values=values, report_id=report_id, keys=keys)
        await self._mark_updated(report_id=report_id, old_rows_ids=old_rows_ids)

    async def _mark_updated(self, report_id: int, old_rows_ids: List[int]) -> None:
        await self.repository.mark_updated_by_report_id(report_id=report_id)
        await self.report_value_service.mark_updated_by_rows_ids(rows_ids=old_rows_ids)
