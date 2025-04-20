from fastapi import APIRouter

router = APIRouter(tags=["Client"])

@router.get("/clients")
async def clients() -> dict[str, str]:
    return {"message": "pass"}