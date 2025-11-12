from datetime import datetime
from typing import TYPE_CHECKING
from typing import List
from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.databases import Base

if TYPE_CHECKING:
    from .report_values import TableReportValue
    from .table_report import TableReport


class TableReportRow(Base):
    """
    Модель названий стобцов отчета

    ## Attrs:
      - id: int - идентификатор
      - unique_value: str - уникальное значение
      - created_at: datetime - дата и время создания
      - updated_at: datetime - дата и время обновления
      - is_deleted: bool - удален или нет
      - report_id: int - идентификатор отчета FK TableReport
      - report: TableReport - связь с отчетом
      - values: List[TableReportValue] - связь со значениями

    """

    __tablename__ = "table_report_row"
    __table_args__ = (UniqueConstraint("id", "unique_value", name="uix_column_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    unique_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("table_report.id", ondelete="CASCADE"), index=True)
    report: Mapped["TableReport"] = relationship("TableReport", back_populates="rows")
    values: Mapped[List["TableReportValue"]] = relationship(
        "TableReportValue",
        back_populates="row",
        cascade="all, delete",
        passive_deletes=True,
    )
