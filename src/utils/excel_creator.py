import uuid
from io import BytesIO
from typing import Any

import pandas as pd
from fastapi import Response


class ExcelCreator:
    def __init__(self, data: dict):
        self.data = data

    async def get_excel_bytes(self) -> bytes:
        """
        Преобразует данные в Excel файл и возвращает байтовую строку.
        """
        columns_metadata = self.data.get("columns_metadata", {}).get("metadata", [])

        rows_data = {}

        for row in self.data.get("rows", []):
            row_id = row.get("unique_value", f"Row_{row.get('id')}")
            row_values = {}

            for value in row.get("values", []):
                column_name = value.get("column_name")
                cell_value = value.get("value")

                processed_value = await self._process_cell_value(cell_value)

                if column_name and column_name in columns_metadata:
                    row_values[column_name] = processed_value

            rows_data[row_id] = row_values

        df = pd.DataFrame.from_dict(rows_data, orient="index")

        for column in columns_metadata:
            if column not in df.columns:
                df[column] = None

        df = df.reindex(columns=columns_metadata)

        output = BytesIO()

        try:
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Данные", index=True, index_label="ID строки")

                worksheet = writer.sheets["Данные"]

                await self._auto_fit_columns(worksheet)

                await self._create_metadata_sheet(writer)

            excel_bytes = output.getvalue()
            return Response(
                content=excel_bytes,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename={str(uuid.uuid4())}"},
            )

        finally:
            output.close()

    async def _process_cell_value(self, value: Any) -> Any:
        if value is None:
            return None

        elif isinstance(value, str):
            if value == "nan":
                return None
            elif value.endswith(".0") and value.replace(".0", "").isdigit():
                return int(float(value))
            elif value.replace(".", "").replace("-", "").isdigit():
                try:
                    return float(value)
                except ValueError:
                    return value
            else:
                return value
        else:
            return value

    async def _auto_fit_columns(self, worksheet):
        """Автоматически подгоняет ширину колонок в Excel."""
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except Exception:
                    pass

            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

    async def _create_metadata_sheet(self, writer):
        """Создает лист с метаданными отчета."""
        metadata = {
            "Параметр": [
                "ID отчета",
                "Название отчета",
                "Дата создания",
                "Дата обновления",
                "ID пользователя",
                "ID шаблона",
                "Всего строк",
                "Колонок в отчете",
            ],
            "Значение": [
                self.data.get("id", ""),
                self.data.get("name", ""),
                self.data.get("created_at", ""),
                self.data.get("updated_at", ""),
                self.data.get("user_id", ""),
                self.data.get("template_id", ""),
                self.data.get("total_rows", ""),
                len(self.data.get("columns_metadata", {}).get("metadata", [])),
            ],
        }

        metadata_df = pd.DataFrame(metadata)
        metadata_df.to_excel(writer, sheet_name="Метаданные", index=False)

        metadata_sheet = writer.sheets["Метаданные"]
        await self._auto_fit_columns(metadata_sheet)
