from typing import Dict
from typing import Generator
from typing import List
from typing import Literal

import pandas as pd
from fastapi import UploadFile
from loguru import logger

from utils.errors import DomainError
from utils.errors import ErrorCodes


class ExcelParser:
    """
    Парсер Excel файлов с поддержкой batched чтения и базовой валидацией.
    Требования:
    - Поддержка форматов .xlsx и .xls
    - Батчинг для больших файлов (batch processing)
    - Валидация структуры файла (наличие данных, корректность формата)
    """

    def __init__(self, file: UploadFile, small_file_bytes: int = 20, batch_size: int = 1000):
        self.file = file
        self.small_bytes = small_file_bytes
        self.batch_size = batch_size
        self.enginie = self._get_engine()
        self.xls = pd.ExcelFile(self.file, engine=self.enginie)

    def _get_engine(self) -> str:
        """
        Внутренний helper для выбора движка чтения в зависимости от расширения.
        Примечание: для .xls нужен пакет xlrd.
        """
        logger.info("Получение движка для парсинга файла")
        match self.file.filename:
            case self.file.filename.endswith(".xlsx"):
                logger.info("Определен тип .xlsx, парсинг через openpyxl")
                return "openpyxl"

            case self.file.filename.endswith(".xls"):
                logger.info("Определен тип .xls, парсинг через xlrd")
                return "xlrd"

            case _:
                logger.error("Ошибка не валидный формат файла")
                raise DomainError(ErrorCodes.INVALID_FILE_FORMAT)

    async def _get_reading_mode(self) -> Literal["sipmle", "batch"]:
        logger.info("Oпределение режима чтения файла")

        if 0 < self.file.size <= self.small_bytes:
            logger.info(f"Размер файла {self.file.size} режим sipmle")
            return "sipmle"

        logger.info(f"Размер файла {self.file.size} режим batch")
        return "batch"

    async def _simple_read(self) -> Generator[pd.DataFrame, None, None]:
        for sheet in self.xls.sheet_names:
            df = self.xls.parse(sheet)
            if df is None or df.empty:
                continue
            yield df
        return

    async def read_batches(self) -> Generator[pd.DataFrame, None, None]:
        for sheet in self.xls.sheet_names:
            df = self.xls.parse(sheet)
            if df is None or df.empty:
                continue
            for start in range(0, len(df), ExcelParser.batch_size):
                batch = df.iloc[start : start + ExcelParser.batch_size].copy()
                yield batch

    async def read_excel(self) -> Generator[pd.DataFrame, None, None]:
        mode = await self._get_reading_mode()
        match mode:
            case "batch":
                df = await self.read_batches()
            case "sipmle":
                df = await self._simple_read()
        valid_df = await self._validate_structure(df)
        return valid_df

    async def _validate_structure(self, df: pd.DataFrame) -> None:
        """
        Проверка базовой структуры DataFrame:
        """
        logger.info("Прверка валидности файла")
        if df is None or df.empty:
            logger.error("Ошибка валидации файл пустой")
            raise DomainError(ErrorCodes.FILE_IS_EMPTY)

    async def extract_metadata(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Возвращает метаданные столбцов файла: список названий столбцов.
        """
        logger.info("Получение метаданных столбцов файла")
        return {"metadata": list(df.columns)}

    async def convert_rows_to_dicts(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """
        Преобразование строк DataFrame в список словарей (значения конвертированы в текст).
        """
        return df.astype(str).to_dict(orient="records")

    async def get_total_rows_count(self, df: pd.DataFrame) -> int:
        return len(self.convert_rows_to_dicts(df=df))
