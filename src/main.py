import uvicorn
from fastapi import FastAPI

import api
from config import settings

import asyncio
from scraper.run import run

app = FastAPI()

app.include_router(api.router)

if __name__ == "__main__":
    asyncio.run(run())
    # uvicorn.run("main:app", reload=True)


