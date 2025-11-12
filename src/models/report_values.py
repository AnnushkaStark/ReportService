from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.databases import Base

if TYPE_CHECKING:
    from .report_rows import TableReportRow


class TableReportValue(Base):
    """
    Модель отчета

    ## Attrs:
        - id: int - идентификатор
        - column_name: str - название столбца
        - value: str - значение столбца
        - created_at: datetime - дата и время создания
        - updated_at: datetime - дата и время обновления
        - row_id: int - идентификатор ряда
          FK TableReportRow
        - row: TableReportRow - связь с рядом
    """

    __tablename__ = "table_report_value"
    __table_args__ = (UniqueConstraint("row_id", "column_name", name="uq_table_report_values_row_column"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    column_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=True)
    row_id: Mapped[int] = mapped_column(Integer, ForeignKey("table_report_row.id", ondelete="CASCADE"), index=True)
    row: Mapped["TableReportRow"] = relationship("TableReportRow", back_populates="values")
