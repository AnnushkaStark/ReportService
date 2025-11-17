from typing import List

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.databases import Base


class AbstactBaseRepository:
    def __init__(self, session: AsyncSession, model: Base):
        self.session = session
        self.model = model

    async def get_all(self) -> List[Base]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, schema: BaseModel) -> Base:
        result = await self.session.execute(insert(self.model).values(schema.model_dump()).returning(self.model))
        return result.scalar()

    async def create_bulk(self, schemas: List[BaseModel]) -> List[Base]:
        data = [s.model_dump() for s in schemas]
        objs = await self.session.execute(insert(self.model).values(data).returning(self.model))
        await self.session.commit()
        return objs.scalars().all()

    async def remove(self, obj_id) -> None:
        await self.session.execute(delete(self.model).where(self.model.id == obj_id))
        await self.session.commit()

    async def get_by_id(self, obj_id: int) -> Base:
        result = await self.session.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalar()
