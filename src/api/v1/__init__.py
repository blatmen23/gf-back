from fastapi import APIRouter

from .client import router as client_router
from .scraper import router as scraper_router

router = APIRouter(prefix="/v1")
router.include_router(client_router, prefix="/client")
router.include_router(scraper_router, prefix="/scraper")

