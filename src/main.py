import os
import uvicorn
from fastapi import FastAPI

DOMAIN = os.environ.get("DOMAIN")
app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
