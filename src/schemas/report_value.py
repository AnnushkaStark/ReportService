from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from schemas import StrOrNone


class ReportValueBase(BaseModel):
    column_name: StrOrNone
    value: Optional[StrOrNone] = Field(default=None)


class ReportValueCreateDB(ReportValueBase):
    row_id: int


class ReportValueResponse(ReportValueBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)
