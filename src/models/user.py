from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.databases import Base


class User(Base):
    """
    Модель пользователя (мок)

    ## Attrs:
        - id: int - идентификатор

    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
