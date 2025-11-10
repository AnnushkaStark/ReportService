from datetime import datetime
from typing import TYPE_CHECKING
from typing import List
from typing import Optional

from sqlalchemy import JSON
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.databases import Base

if TYPE_CHECKING:
    from .report_rows import TableReportRow


class TableReport(Base):
    """
    Модель отчета

    ## Attrs:
        - id: int - идентификатор
        - name: str - название
        - created_at: datetime - дата и время создания
        - updated_at: datetime - дата и время обновления
        - user_id: int - идентификатор пользоватея
          FK user
        - template_id: int - идентификатор ресурса
          FK template
        - rows: List[TableReportRows] - связь с названиями столбцов exel
    """

    __tablename__ = "table_report"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey("template.id", ondelete="CASCADE"))
    columns_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    total_rows: Mapped[int] = mapped_column(Integer, default=0)
    additional_params: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    rows: Mapped[List["TableReportRow"]] = relationship(
        "TableReportRow",
        back_populates="report",
        cascade="all, delete",
        passive_deletes=True,
    )
