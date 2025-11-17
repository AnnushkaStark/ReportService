from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReport
from models import TableReportRow
from models import TableReportValue
from utils.errors import ErrorCodes

from ..fixtures.test_files.test_excel import _image_dir

ROOT_URL = "/report_service/api/report/"


class TestUpdate:
    async def test_update_append_success(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        table_report_fixture: TableReport,
        table_report_row_fixture: TableReportRow,
        table_report_value_fixture: TableReportValue,
    ) -> None:
        response = await http_client.put(
            f"{ROOT_URL}{table_report_fixture.id}/",
            params={"mode": "append"},
            files={"file": open(_image_dir / "tst2.xlsx", "rb")},
        )
        assert response.status_code == 200

        await async_session.close()
        updated_report = await async_session.get(TableReport, table_report_fixture.id)
        assert updated_report.updated_at is not None

        rows = await async_session.execute(
            select(TableReportRow).where(TableReportRow.report_id == table_report_fixture.id)
        )
        rows = rows.scalars().all()
        assert len(rows) == 1

        rows_ids = [row.id for row in rows]
        new_values = await async_session.execute(select(TableReportValue).where(TableReportValue.row_id.in_(rows_ids)))
        new_values = new_values.scalars().all()
        assert len(new_values) > 1

    async def test_update_replace_succes(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        table_report_fixture: TableReport,
        table_report_row_fixture: TableReportRow,
        table_report_value_fixture: TableReportValue,
    ) -> None:
        response = await http_client.put(
            f"{ROOT_URL}{table_report_fixture.id}/",
            params={"mode": "replace"},
            files={"file": open(_image_dir / "tst2.xlsx", "rb")},
        )
        assert response.status_code == 200

        await async_session.close()
        updated_report = await async_session.get(TableReport, table_report_fixture.id)
        assert updated_report.updated_at is not None

        rows = await async_session.execute(
            select(TableReportRow).where(TableReportRow.report_id == table_report_fixture.id)
        )
        rows = rows.scalars().all()
        assert len(rows) > 1
        assert rows[0].is_deleted is True

    async def test_update_with_invalid_file_format(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        table_report_fixture: TableReport,
    ) -> None:
        response = await http_client.put(
            f"{ROOT_URL}{table_report_fixture.id}/",
            params={"mode": "replace"},
            files={"file": open(_image_dir / "test.docs", "rb")},
        )
        assert response.status_code == 422

        response_data = response.json()
        assert response_data["detail"] == ErrorCodes.INVALID_FILE_FORMAT.value

        await async_session.close()
        not_updated_report = await async_session.get(TableReport, table_report_fixture.id)
        assert not_updated_report.updated_at is None

    async def test_update_with_empty_file(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        table_report_fixture: TableReport,
    ) -> None:
        response = await http_client.put(
            f"{ROOT_URL}{table_report_fixture.id}/",
            params={"mode": "replace"},
            files={"file": open(_image_dir / "empty.xlsx", "rb")},
        )
        assert response.status_code == 422

        response_data = response.json()
        assert response_data["detail"] == ErrorCodes.FILE_IS_EMPTY.value

        await async_session.close()
        not_updated_report = await async_session.get(TableReport, table_report_fixture.id)
        assert not_updated_report.updated_at is None

    async def test_update_invalid_report_id(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
    ) -> None:
        response = await http_client.put(
            f"{ROOT_URL}{11}/", params={"mode": "replace"}, files={"file": open(_image_dir / "empty.xlsx", "rb")}
        )
        assert response.status_code == 404

        response_data = response.json()
        assert response_data["detail"] == ErrorCodes.REPORT_NOT_FOUND.value
