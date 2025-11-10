from abc import ABC
from abc import abstractmethod
from typing import List

from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.databases import Base


class AbstactBaseRepository(ABC):
    def __init__(self, session: AsyncSession, model: Base):
        self.session = session
        self.model = model

    @abstractmethod
    async def get_all(self) -> List[Base]:
        result = await self.session.execute(select(self.model))
        return result.scalars().first()

    @abstractmethod
    async def create(self, schema: BaseModel) -> Base:
        return await self.session.execute(insert(self.model).values(schema.model_dump()).returning(self.model))

    @abstractmethod
    async def create_bulk(self, schemas: List[BaseModel]) -> List[Base]:
        data = [s.model_dump() for s in schemas]
        stmt = insert(self.model).values(data).returning(self.model)
        res = await self.session.execute(stmt)
        objs = res.scalars().all()
        await self.session.commit()
        return objs
