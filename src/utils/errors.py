import enum
from typing import Optional

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Error(BaseModel):
    detail: str


class ErrorCodes(enum.Enum):
    INVALID_FILE_FORMAT = "Неподдерживаемый формат файла"
    FILE_IS_EMPTY = "Невозможно прочитать - файл пустой"
    NOT_ALL_COILUMS_HAS_UNIQUE_NAMES = "Не все названия столбцов уникальны"
    REPORT_NOT_FOUND = "Отчет не найден"


class DomainError(Exception):
    code: ErrorCodes

    def __init__(self, code: ErrorCodes, message: Optional[str] = None):
        self.code = code
        super().__init__(message)


async def domain_error_exception_handler(request: Request, exc: DomainError):
    ERROR_STATUS_MAP = {
        ErrorCodes.INVALID_FILE_FORMAT: 422,
        ErrorCodes.NOT_ALL_COILUMS_HAS_UNIQUE_NAMES: 422,
        ErrorCodes.FILE_IS_EMPTY: 422,
        ErrorCodes.REPORT_NOT_FOUND: 400,
    }

    status_code = ERROR_STATUS_MAP.get(exc.code, 500)

    return JSONResponse(
        status_code=status_code,
        content={"message": exc.code.value},
    )


class BaseError(BaseModel):
    message: str


def create_response_schema(description: str):
    return dict(
        model=BaseError,
        description=description,
    )


def _format_description(codes) -> str:
    return "".join(f"<br />{code.value}" for code in codes)[len("<br />") :]


def errs(**_codes):
    ret = dict()
    processed = set()

    for status_codes, codes in _codes.items():
        if not hasattr(codes, "__iter__"):
            codes = (codes,)

        if set(codes) & processed:
            raise RuntimeError("Error codes duplicated")

        processed |= set(codes)

        status_code = int(status_codes.strip("e"))

        ret[status_code] = dict(
            model=BaseError,
            description=_format_description(codes),
        )
    return ret
