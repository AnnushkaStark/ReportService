from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReport
from utils.errors import ErrorCodes

from ..fixtures.test_files.test_excel import _image_dir

ROOT_URL = "/report_service/api/report/"


class TestCreate:
    async def test_create_success(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
    ) -> None:
        response = await http_client.post(
            ROOT_URL, data={"name": "test_report"}, files={"file": open(_image_dir / "отчет для теста.xlsx", "rb")}
        )
        assert response.status_code == 201

        await async_session.close()
        created_report = await async_session.execute(select(TableReport).where(TableReport.name == "test_report"))
        created_report = created_report.scalar_one_or_none()
        assert created_report is not None

    async def test_create_with_invalid_file_format(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
    ) -> None:
        response = await http_client.post(
            ROOT_URL, data={"name": "test_report_docs"}, files={"file": open(_image_dir / "test.docs", "rb")}
        )
        assert response.status_code == 422

        response_data = response.json()
        assert response_data["detail"] == ErrorCodes.INVALID_FILE_FORMAT.value

        await async_session.close()
        not_created_report = await async_session.execute(
            select(TableReport).where(TableReport.name == "test_report_docs")
        )
        not_created_report = not_created_report.scalar_one_or_none()
        assert not_created_report is None

    async def test_create_with_empty_file(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
    ) -> None:
        response = await http_client.post(
            ROOT_URL, data={"name": "test_report_empty"}, files={"file": open(_image_dir / "empty.xlsx", "rb")}
        )
        assert response.status_code == 422

        response_data = response.json()
        assert response_data["detail"] == ErrorCodes.FILE_IS_EMPTY.value

        await async_session.close()
        not_created_report = await async_session.execute(
            select(TableReport).where(TableReport.name == "test_report_empty")
        )
        not_created_report = not_created_report.scalar_one_or_none()
        assert not_created_report is None

    async def test_create_with_not_unique_columns(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
    ) -> None:
        response = await http_client.post(
            ROOT_URL,
            data={"name": "test_report_not_unique"},
            files={"file": open(_image_dir / "not_unique_rows.xlsx", "rb")},
        )
        assert response.status_code == 422

        response_data = response.json()
        assert response_data["detail"] == ErrorCodes.NOT_ALL_COILUMS_HAS_UNIQUE_NAMES.value
        await async_session.close()
        not_created_report = await async_session.execute(
            select(TableReport).where(TableReport.name == "test_report_not_unique")
        )
        not_created_report = not_created_report.scalar_one_or_none()
        assert not_created_report is None
