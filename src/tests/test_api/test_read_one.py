from httpx import AsyncClient

from models import TableReport
from models import TableReportRow
from models import TableReportValue
from models import User
from utils.errors import ErrorCodes

ROOT_URL = "/report_service/api/report/"


class TestReadtableReport:
    async def test_read_success(
        self,
        http_client: AsyncClient,
        table_report_fixture: TableReport,
        table_report_row_fixture: TableReportRow,
        table_report_value_fixture: TableReportValue,
    ) -> None:
        response = await http_client.get(f"{ROOT_URL}full_data/{table_report_fixture.id}/", params={"mode": "json"})
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["id"] == table_report_fixture.id
        assert len(response_data["rows"]) == 1
        assert response_data["rows"][0]["id"] == table_report_row_fixture.id
        assert len(response_data["rows"][0]["values"]) == 1
        assert response_data["rows"][0]["values"][0]["id"] == table_report_value_fixture.id

    async def test_read_with_invalid_id(
        self,
        http_client: AsyncClient,
    ) -> None:
        response = await http_client.get(f"{ROOT_URL}full_data/{11}/", params={"mode": "json"})

        assert response.status_code == 404

        response_data = response.json()
        assert response_data["message"] == ErrorCodes.REPORT_NOT_FOUND.value

    async def test_read_in_excel_success(
        self,
        http_client: AsyncClient,
        table_report_fixture: TableReport,
        table_report_row_fixture: TableReportRow,
        table_report_value_fixture: TableReportValue,
    ) -> None:
        response = await http_client.get(f"{ROOT_URL}full_data/{table_report_fixture.id}/", params={"mode": "excel"})
        assert response.status_code == 200
        assert "attachment" in response.headers["Content-Disposition"]
