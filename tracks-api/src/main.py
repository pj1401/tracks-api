"""
The starting point of the API.
module: src/main.py
"""

from fastapi import FastAPI
from .routers.api.api_router import api_router

app = FastAPI()


app.include_router(api_router, prefix="/api")
