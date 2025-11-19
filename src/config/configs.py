from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseSetting):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


class SentrySettings(BaseSetting):
    SENTRY_DNS: str = None


sentry_settings = SentrySettings()
db_settings = DBSettings()
