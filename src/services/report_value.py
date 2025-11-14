from typing import List

from repositories.report_value import ReportValueRepository
from schemas import StatValue
from schemas.report_value import ReportValueCreateDB


class ReportValueService:
    def __init__(self, repository: ReportValueRepository):
        self.repository = repository

    async def _get_schemas_multi(self, values: List[str], columns: List[str], rows_ids: List[int]):
        prepared_data = []
        for i, row_id in enumerate(rows_ids):
            for j, column in enumerate(columns):
                value_index = i * len(columns) + j

                if value_index < len(values):
                    prepared_data.append({"row_id": row_id, "column_name": column, "value": values[value_index]})

        return [ReportValueCreateDB(**item) for item in prepared_data]

    async def create_multi(self, values: List[str], columns: List[str], rows_ids: List[int]) -> None:
        await self.repository.create_bulk(
            schemas=await self._get_schemas_multi(values=values, rows_ids=rows_ids, columns=columns)
        )

    async def get_stat_schema(self, rows_ids: List[int]) -> StatValue:
        return StatValue(
            total_values=await self.repository.get_total_value_count_by_rows_ids(rows_ids=rows_ids),
            not_null_values=await self.repository.get_unique_value_count_by_rows_ids(rows_ids=rows_ids),
            null_values=await self.repository.get_nullable_value_count_by_rows_ids(rows_ids=rows_ids),
            updated_values=await self.repository.get_updated_value_count_by_rows_ids(rows_ids=rows_ids),
        )

    async def mark_updated_by_rows_ids(self, rows_ids: List[int]) -> None:
        pass
