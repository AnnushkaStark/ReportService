import sentry_sdk
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.router import api_router as report_service_router
from config.configs import sentry_settings
from utils.errors import DomainError
from utils.errors import domain_error_exception_handler

sentry_sdk.init(
    dsn=sentry_settings.SENTRY_DNS,
    send_default_pii=True,
)

app = FastAPI(
    title="ReportService",
    openapi_url="/report_service/openapi.json",
    docs_url="/report_service/docs",
    exception_handlers={DomainError: domain_error_exception_handler},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(report_service_router, prefix="/report_service")
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        proxy_headers=True,
    )
