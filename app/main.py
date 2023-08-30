import logging
import sys

import uvicorn
from fastapi import FastAPI
from routes import router

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI()

app.include_router(router, prefix="")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level=logging.INFO)
