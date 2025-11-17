from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReport
from utils.errors import ErrorCodes

ROOT_URL = "/report_service/api/report/"


class TestRemoveReport:
    async def test_remove_success(
        self,
        http_client: AsyncClient,
        table_report_fixture: TableReport,
        async_session: AsyncSession,
    ) -> None:
        response = await http_client.delete(f"{ROOT_URL}{table_report_fixture.id}/")
        assert response.status_code == 204

        await async_session.close()
        deleted_report = await async_session.get(TableReport, table_report_fixture.id)
        assert deleted_report is None

    async def test_remove_with_invalid_id(
        self,
        http_client: AsyncClient,
        table_report_fixture: TableReport,
        async_session: AsyncSession,
    ) -> None:
        response = await http_client.delete(f"{ROOT_URL}{11}/")

        assert response.status_code == 404

        response_data = response.json()
        assert response_data["detail"] == ErrorCodes.REPORT_NOT_FOUND.value

        not_deleted_report = await async_session.get(TableReport, table_report_fixture.id)
        assert not_deleted_report is not None
