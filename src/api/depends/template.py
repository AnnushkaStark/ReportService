from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends.database import get_async_db
from repositories.template import TempltateRepository
from services.template import TemplateService


async def get_template_repository(session: AsyncSession = Depends(get_async_db)) -> TempltateRepository:
    return TempltateRepository(session=session)


async def get_template_service(repository: TempltateRepository = Depends(get_template_repository)) -> TemplateService:
    return TemplateService(repository=repository)


async def get_template_id(service: TemplateService = Depends(get_template_service)) -> int:
    template = await service.get_or_create()
    return template.id
