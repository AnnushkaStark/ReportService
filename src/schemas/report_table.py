from pydantic import BaseModel


class TableReportBase(BaseModel):
    user_id: int
    template_id: int
    total_rows: int
    columns_metadata: dict
    additional_params: dict
