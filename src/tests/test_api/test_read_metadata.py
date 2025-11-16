from httpx import AsyncClient

from models import TableReport
from models import User
from utils.errors import ErrorCodes

ROOT_URL = "/report_service/api/report/"


class TestReadMetadata:
    async def test_read_success(
        self,
        http_client: AsyncClient,
        table_report_fixture: TableReport,
    ) -> None:
        response = await http_client.get(f"{ROOT_URL}{table_report_fixture.id}/metadata/")
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["id"] == table_report_fixture.id

    async def test_read_with_invalid_id(
        self,
        http_client: AsyncClient,
    ) -> None:
        response = await http_client.get(f"{ROOT_URL}{11}/metadata/")

        assert response.status_code == 404

        response_data = response.json()
        assert response_data["detail"] == ErrorCodes.REPORT_NOT_FOUND.value
