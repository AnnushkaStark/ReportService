from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def triggered_error():
    return 1 / 0
