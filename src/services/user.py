from models import User
from repositories.user import UserRepository
from schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository, schema: UserCreate):
        self.repository = repository
        self.schema = schema

    async def get_or_create(self) -> User:
        users = await self.repository.get_all()
        if len[users]:
            return users[0]
        return await self.repository.create(schema=self.schema.model_dump())
