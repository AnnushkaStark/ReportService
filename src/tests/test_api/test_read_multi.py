from httpx import AsyncClient

from models import TableReport

ROOT_URL = "/report_service/api/report/"


class TestReadMetadata:
    async def test_read_success(
        self,
        http_client: AsyncClient,
        table_report_fixture: TableReport,
    ) -> None:
        response = await http_client.get(ROOT_URL)
        assert response.status_code == 200

        response_data = response.json()
        assert len(response_data["items"]) == 1
        assert response_data["items"][0]["id"] == table_report_fixture.id
