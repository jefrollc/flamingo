from typing import List

from fastapi import FastAPI

import database

app = FastAPI()

@app.get("/")
async def index():
    return {"ping": "pong"}
