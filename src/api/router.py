from fastapi import APIRouter

from api.endpoints.report import router as report_router
from api.endpoints.sentry_health import router as senttry_health_router

api_router = APIRouter(prefix="/api")

api_router.include_router(report_router, prefix="/report", tags=["Report"])
api_router.include_router(senttry_health_router, prefix="/sentry_health", tags=["SentryHealth"])
