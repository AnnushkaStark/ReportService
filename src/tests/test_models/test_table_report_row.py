from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReportRow


class TestTableReportRowModel:
    async def test_fields(self, async_session: AsyncSession) -> None:
        concurrent_fields_name = [i.name for i in TableReportRow.__table__.columns]
        related_fields = [i._dependency_processor.key for i in TableReportRow.__mapper__.relationships]
        all_model_fields = concurrent_fields_name + related_fields
        schema_fields_name = {
            "unique_value",
            "created_at",
            "updated_at",
            "is_deleted",
            "report_id",
            "report",
            "values",
        }
        for field in schema_fields_name:
            assert field in all_model_fields, "Нет необходимого поля %s" % field
