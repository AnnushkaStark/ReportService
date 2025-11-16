from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReport


class TestTableReportModel:
    async def test_fields(self, async_session: AsyncSession) -> None:
        concurrent_fields_name = [i.name for i in TableReport.__table__.columns]
        related_fields = [i._dependency_processor.key for i in TableReport.__mapper__.relationships]
        all_model_fields = concurrent_fields_name + related_fields
        schema_fields_name = {
            "name",
            "created_at",
            "updated_at",
            "user_id",
            "template_id",
            "columns_metadata",
            "total_rows",
            "additional_params",
            "rows",
        }
        for field in schema_fields_name:
            assert field in all_model_fields, "Нет необходимого поля %s" % field
