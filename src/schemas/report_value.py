from pydantic import BaseModel


class ReportValueBase(BaseModel):
    column_name: str
    value: str


class ReportValueCreateDB(ReportValueBase):
    row_id: int
