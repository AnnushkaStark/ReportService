import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    """Обработчик для перехвата стандартных логов Python в loguru"""

    def emit(self, record: logging.LogRecord) -> None:
        # Получаем соответствующий уровень loguru
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        # Находим caller frame для правильного отображения источника
        frame, depth = logging.currentframe(), 6
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    """Настройка логирования для перехвата всех логов в loguru"""
    # Удаляем стандартные обработчики loguru
    logger.remove()
    # Настраиваем loguru форматирование
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "{message}"
    )
    # Добавляем обработчик для консоли
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True,
        diagnose=True,
        backtrace=True,
    )
    # Перехватываем все стандартные логгеры Python
    intercept_handler = InterceptHandler()
    # Список логгеров для перехвата
    loggers_to_intercept = [
        "",  # root logger
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "starlette",
        "multipart",
        "multipart.multipart",
        "urllib3",
        "httpx",
        "asyncio",
        "aiohttp",
        "redis",
        "sqlalchemy",
        "sqlalchemy.engine",
        "sqlalchemy.pool",
        "alembic",
        "advanced_alchemy",
        "apscheduler",
        "apscheduler.scheduler",
        "apscheduler.executors",
        "apscheduler.jobstores",
    ]
    # Настраиваем перехват для каждого логгера
    for logger_name in loggers_to_intercept:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [intercept_handler]
        logging_logger.setLevel("INFO")
        logging_logger.propagate = False
    logging.getLogger().setLevel("INFO")
    # Логируем успешную инициализацию
    logger.info("🚀 Система логирования успешно инициализирована.")
    logger.info("📊 Уровень логгирования консоли: INFO")

    """Конфигурация для перехвата логов uvicorn"""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "default": {
                "class": "config.log_conf.InterceptHandler",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }
