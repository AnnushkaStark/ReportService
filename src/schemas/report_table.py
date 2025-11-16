from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from schemas.report_row import ReportRowFullResponse


class TableReportBase(BaseModel):
    user_id: int
    template_id: int
    total_rows: int
    name: str
    columns_metadata: Optional[dict] = Field(default=None)
    additional_params: Optional[dict] = Field(default=None)


class TableReportResponse(TableReportBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)


class TableReportFullResponse(TableReportResponse):
    rows: List[ReportRowFullResponse]
