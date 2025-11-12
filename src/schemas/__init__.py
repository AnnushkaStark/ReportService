from typing import List

from pydantic import BaseModel


class UserCreate(BaseModel):
    pass


class TemplateCreate(BaseModel):
    pass


class PaginationBase(BaseModel):
    limit: int
    offset: int
    count: int


class PaginationResponse[T](BaseModel):  # noqa: F821
    @classmethod
    def create(
        cls,
        limit: int,
        offset: int,
        count: int,
        items: List[T],  # noqa: F821
    ):
        return cls(
            pagination=PaginationBase(limit=limit, offset=offset, count=count),
            items=items,
        )

    pagination: PaginationBase
    items: List[T]  # noqa: F821


class StatValue(BaseModel):
    row_id: int
    total_values: int
    not_null_values: int
    null_values: int
    updated_values: int


class StatsRow(BaseModel):
    report_id: int
    not_null_values: int
    null_values: int
    deleted_values: int
    updated_values: int
    value_stats: List[StatValue]


class ReportStats(BaseModel):
    report_id: int
    total_rows: int
    rows_stats: List[StatsRow]
