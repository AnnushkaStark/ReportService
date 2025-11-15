from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from schemas import StrOrNone
from schemas.report_value import ReportValueResponse


class ReportRowBase(BaseModel):
    unique_value: StrOrNone


class ReportRowCreateDB(ReportRowBase):
    report_id: int


class ReportRowResponse(ReportRowBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)
    is_deleted: bool


class ReportRowFullResponse(ReportRowResponse):
    values: List[ReportValueResponse]
