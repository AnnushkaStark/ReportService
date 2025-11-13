from collections import OrderedDict
from contextlib import asynccontextmanager
from typing import Literal
from typing import Optional
from typing import Union

import pandas as pd
from fastapi import UploadFile

from models import TableReport
from repositories.report_table import TableReportRepository
from schemas import ReportStats
from schemas.report_table import TableReportBase
from schemas.report_table import TableReportFullResponse
from services.report_row import ReportRowService
from utils.errors import DomainError
from utils.errors import ErrorCodes
from utils.excel_creator import ExcelCreator
from utils.excel_parser import ExcelParser
from utils.types import Ok


class TableReportService:
    def __init__(self, repository: TableReportRepository, report_row_service: ReportRowService):
        self.repository = repository
        self.report_row_service = report_row_service

    @asynccontextmanager
    async def _get_parser(self, file: UploadFile) -> ExcelParser:
        parser = ExcelParser(file=file)
        yield parser

    @asynccontextmanager
    async def _get_creator(self, data: dict) -> ExcelCreator:
        creator = ExcelCreator(data=data)
        yield creator

    async def _get_schema(
        self, uer_id: int, template_id: int, additional_params: dict, df: pd.DataFrame, parser: ExcelParser, name: str
    ) -> TableReportBase:
        return TableReportBase(
            name=name,
            user_id=uer_id,
            template_id=template_id,
            columns_metadata=await parser.extract_metadata(df=df),
            total_rows=await parser.get_total_rows_count(df=df),
            additional_params=additional_params,
        )

    async def create(self, file: UploadFile, uer_id: int, template_id: int, additional_params: dict) -> TableReport:
        async with self._get_parser(file) as parser:
            async for df in parser.read_excel():
                schema = await self._get_schema(
                    uer_id=uer_id,
                    template_id=template_id,
                    additional_params=additional_params,
                    df=df,
                    parser=parser,
                    name=file.filename,
                )
                report = await self.repository.create(schema=schema)
                df_dict = await parser.convert_rows_to_dicts(df)
                keys = list(OrderedDict.fromkeys(key for d in df_dict for key in d.keys()))
                values = [value for d in df_dict for value in d.values()]
                rows_ids = await self.report_row_service.create_rows_multi(report_id=report.id, values=keys)
                await self.report_row_service._create_row_values(keys=keys, values=values, row_ids=rows_ids)
                return "Ok"

    async def get_report_metadata(self, obj_id: int, user_id: int) -> Optional[TableReport]:
        return await self.repository.get_by_id_and_user_id(obj_id=obj_id, user_id=user_id)

    async def _get_full_in_json(self, obj_id: int, user_id: int) -> Optional[TableReport]:
        if found_report := await self.repository.get_full_by_id_and_user_id(obj_id=obj_id, user_id=user_id):
            return found_report
        raise DomainError(ErrorCodes.REPORT_NOT_FOUND)

    async def _get_full_id_excel(self, obj_id: int, user_id: int) -> bytes:
        found_report = await self._get_full_in_json(obj_id=obj_id, user_id=user_id)
        report_schema = TableReportFullResponse.model_validate(found_report, from_attributes=True)
        async with self._get_creator(data=report_schema.model_dump()) as creator:
            return await creator.get_excel_bytes()

    async def get_table_report_full_data(
        self, obj_id: int, user_id: int, mode: Literal["excel", "json"]
    ) -> Optional[Union[TableReport, bytes]]:
        match mode:
            case "json":
                return await self._get_full_in_json(obj_id=obj_id, user_id=user_id)
            case "excel":
                return await self._get_full_id_excel(obj_id=obj_id, user_id=user_id)

    async def remove(self, obj_id) -> Ok:
        await self.repository.remove(obj_id=obj_id)
        return "Ok"

    async def get_stats(self, report_id: int, user_id: int) -> ReportStats:
        found_report = await self.repository.get_with_row_ids(report_id=report_id, user_id=user_id)
        if not found_report:
            raise DomainError(ErrorCodes.REPORT_NOT_FOUND)
        return ReportStats(
            report_id=found_report.id,
            total_rows=found_report.total_rows,
            rows_stats=await self.report_row_service.get_stats_schema(
                report_id=found_report.id, rows_ids=found_report.rows
            ),
        )
