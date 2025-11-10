from models import Template
from repositories.template import TempltateRepository
from schemas import TemplateCreate


class TemplateService:
    def __init__(self, repository: TempltateRepository, schema: TemplateCreate):
        self.repository = repository
        self.schema = schema

    async def get_or_create(self) -> Template:
        templates = await self.repository.get_all()
        if len[templates]:
            return templates[0]
        return await self.repository.create(schema=self.schema.model_dump())
