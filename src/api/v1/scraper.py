from fastapi import APIRouter

router = APIRouter(tags=["Scraper"])

@router.get("/scrapers")
async def scrappers() -> dict[str, str]:
    return {"message": "pass"}