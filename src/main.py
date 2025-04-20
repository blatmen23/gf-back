import uvicorn
from fastapi import FastAPI

import api
from config import settings

app = FastAPI()

app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


