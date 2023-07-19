import os
import uvicorn
from fastapi import FastAPI

from routes import router

DOMAIN = os.environ.get("DOMAIN")
app = FastAPI()

app.include_router(router, prefix="/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
