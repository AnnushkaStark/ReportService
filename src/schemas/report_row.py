from pydantic import BaseModel


class ReportRowBase(BaseModel):
    unique_value: str


class ReportRowCreateDB(ReportRowBase):
    report_id: int
