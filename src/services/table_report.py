from contextlib import asynccontextmanager

import pandas as pd
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

    @asynccontextmanager
    async def _get_parser(file: UploadFile) -> ExcelParser:
        parser = ExcelParser(file=file)
        yield parser

    async def _get_schema(
        self, uer_id: int, template_id: int, additional_params: dict, df: pd.DataFrame, parser: ExcelParser
    ) -> TableReportBase:
        return TableReportBase(
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
                    uer_id=uer_id, template_id=template_id, additional_params=additional_params, df=df, parser=parser
                )
                report = await self.repository.create(schema=schema)
                df_dict = await parser.convert_rows_to_dicts(df)
                rows = await self.report_row_service.create_rows_multi(report_id=report.id, values=[df_dict.keys()])
                await self.report_row_service._create_row_values(df_dict=df_dict, row_ids=[row.id for row in rows])
