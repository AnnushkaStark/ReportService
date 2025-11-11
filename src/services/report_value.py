from typing import List

from repositories.report_value import ReportValueRepository
from schemas.report_value import ReportValueCreateDB


class ReportValueService:
    def __init__(self, repository: ReportValueRepository):
        self.repository = repository

    async def _get_schemas_multi(self, values: List[tuple]):
        return [ReportValueCreateDB(value[1], **value[0]) for value in values]

    async def create_multi(self, values: List[tuple]) -> None:
        await self.repository.create_bulk(schemas=await self._get_schemas_multi(values=values))
