from datetime import datetime

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from database.databases import Base
from models import TableReport
from models import TableReportRow
from models import TableReportValue
from models import Template
from models import User


async def _add_to_session(session: AsyncSession, model_obj: Base) -> Base:
    session.add(model_obj)
    await session.commit()
    await session.refresh(model_obj)
    return model_obj


@pytest_asyncio.fixture
async def user_fixture(
    async_session: AsyncSession,
) -> User:
    user = User()
    return await _add_to_session(session=async_session, model_obj=user)


@pytest_asyncio.fixture
async def template_fixture(
    async_session: AsyncSession,
) -> Template:
    template = Template()
    return await _add_to_session(session=async_session, model_obj=template)


@pytest_asyncio.fixture
async def table_report_fixture(
    async_session: AsyncSession, user_fixture: User, template_fixture: Template
) -> TableReport:
    report = TableReport(
        name="test name", created_at=datetime.now(), user_id=user_fixture.id, template_id=template_fixture.id
    )
    return await _add_to_session(session=async_session, model_obj=report)


@pytest_asyncio.fixture
async def table_report_row_fixture(
    async_session: AsyncSession,
    table_report_fixture: TableReport,
) -> TableReportRow:
    table_row = TableReportRow(unique_value="test", created_at=datetime.now(), report_id=table_report_fixture.id)
    return await _add_to_session(session=async_session, model_obj=table_row)


@pytest_asyncio.fixture
async def table_report_value_fixture(
    async_session: AsyncSession, table_report_row_fixture: TableReportRow
) -> TableReportValue:
    report_value = TableReportValue(column_name="test", created_at=datetime.now(), row_id=table_report_row_fixture.id)
    return await _add_to_session(session=async_session, model_obj=report_value)
