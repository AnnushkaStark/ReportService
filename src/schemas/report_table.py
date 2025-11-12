from typing import List

from pydantic import BaseModel

from schemas.report_row import ReportRowFullResponse


class TableReportBase(BaseModel):
    user_id: int
    template_id: int
    total_rows: int
    name: str
    columns_metadata: dict
    additional_params: dict


class TableReportResponse(TableReportBase):
    id: int


class TableReportFullResponse(TableReportResponse):
    rows: List[ReportRowFullResponse]
