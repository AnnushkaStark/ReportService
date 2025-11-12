from pydantic import BaseModel


class ReportValueBase(BaseModel):
    column_name: str
    value: str = None


class ReportValueCreateDB(ReportValueBase):
    row_id: int
