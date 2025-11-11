from fastapi import APIRouter

from api.endpoints.report import router as report_router

api_router = APIRouter(prefix="/api")

api_router.include_router(report_router, prefix="/report", tags=["Report"])
