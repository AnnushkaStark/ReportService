from typing import List

from pydantic import BaseModel

from schemas.report_value import ReportValueResponse


class ReportRowBase(BaseModel):
    unique_value: str


class ReportRowCreateDB(ReportRowBase):
    report_id: int


class ReportRowResponse(ReportRowBase):
    id: int


class ReportRowFullResponse(ReportRowResponse):
    values: List[ReportValueResponse]
