import uuid
from io import BytesIO
from typing import Any

import pandas as pd
from fastapi import Response
from loguru import logger


class ExcelCreator:
    """
    Класс для создание excel файла из json формата
    """

    def __init__(self, data: dict):
        self.data = data

    async def get_excel_bytes(self) -> bytes:
        """
        Преобразует данные в Excel файл и возвращает байтовую строку.
        - returns: bytes
        """
        logger.info("Cоздание метдаданных файла")
        columns_metadata = self.data.get("columns_metadata", {}).get("metadata", [])

        rows_data = {}
        logger.info("Cоздание рядов excel таблицы")
        for row in self.data.get("rows", []):
            row_id = row.get("unique_value", f"Row_{row.get('id')}")
            row_values = {}

            for value in row.get("values", []):
                logger.info("Cоздание значений excel таблицы")
                column_name = value.get("column_name")
                cell_value = value.get("value")

                processed_value = await self._process_cell_value(cell_value)

                if column_name and column_name in columns_metadata:
                    row_values[column_name] = processed_value

            rows_data[row_id] = row_values

        logger.info("Cоздание датафрейма")
        df = pd.DataFrame.from_dict(rows_data, orient="index")

        for column in columns_metadata:
            if column not in df.columns:
                df[column] = None

        df = df.reindex(columns=columns_metadata)

        logger.info("Cоздание выходного байтового формата")
        output = BytesIO()

        try:
            logger.info("Запись данных в excel")
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Данные", index=True, index_label="ID строки")

                worksheet = writer.sheets["Данные"]

                await self._auto_fit_columns(worksheet)

                await self._create_metadata_sheet(writer)

            excel_bytes = output.getvalue()
            logger.info("Файл excel подготовлен для скачивания")
            return Response(
                content=excel_bytes,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename={str(uuid.uuid4())}"},
            )

        finally:
            output.close()

    async def _process_cell_value(self, value: Any) -> Any:
        """
        Преобразование значений для записи в excel
        - args: Any
        - returns: Any
        - raises: ValueError
        """
        logger.info("Преобразование значений для записи в excel")
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
        logger.info("Автоматическое определение ширины колонок excel")
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
        logger.info("Cоздание листа с метаданными")
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
