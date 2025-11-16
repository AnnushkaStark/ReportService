from sqlalchemy.ext.asyncio import AsyncSession

from models import TableReportValue


class TestTableReportValueModel:
    async def test_fields(self, async_session: AsyncSession) -> None:
        concurrent_fields_name = [i.name for i in TableReportValue.__table__.columns]
        related_fields = [i._dependency_processor.key for i in TableReportValue.__mapper__.relationships]
        all_model_fields = concurrent_fields_name + related_fields
        schema_fields_name = {
            "column_name",
            "created_at",
            "updated_at",
            "value",
            "row_id",
            "row",
        }
        for field in schema_fields_name:
            assert field in all_model_fields, "Нет необходимого поля %s" % field
