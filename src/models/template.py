from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.databases import Base


class Template(Base):
    """
    Модель template (мок)

    ## Attrs:
        - id: int - идентификатор

    """

    __tablename__ = "tepmplate"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
