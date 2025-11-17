from httpx import AsyncClient

from models import TableReport
from models import TableReportRow
from models import TableReportValue
from utils.errors import ErrorCodes

ROOT_URL = "/report_service/api/report/"


class TestReadTableReport:
    async def test_read_success(
        self,
        http_client: AsyncClient,
        table_report_fixture: TableReport,
        table_report_row_fixture: TableReportRow,
        table_report_value_fixture: TableReportValue,
    ) -> None:
        response = await http_client.get(f"{ROOT_URL}{table_report_fixture.id}/stats/")
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["total_rows"] == 1
        assert response_data["rows_stats"]["not_null_values"] == 1
        assert response_data["rows_stats"]["null_values"] == 0
        assert response_data["rows_stats"]["deleted_values"] == 0
        assert response_data["rows_stats"]["updated_values"] == 0
        assert response_data["rows_stats"]["value_stats"]["total_values"] == 1
        assert response_data["rows_stats"]["value_stats"]["not_null_values"] == 1
        assert response_data["rows_stats"]["value_stats"]["null_values"] == 0
        assert response_data["rows_stats"]["value_stats"]["updated_values"] == 0

    async def test_read_with_invalid_id(
        self,
        http_client: AsyncClient,
    ) -> None:
        response = await http_client.get(f"{ROOT_URL}{11}/stats/")

        assert response.status_code == 404

        response_data = response.json()
        assert response_data["detail"] == ErrorCodes.REPORT_NOT_FOUND.value
