"""
The router that registers the api routes.
module: src/routers/api/api_router.py
"""

import os
from fastapi import APIRouter
from .v1.v1_router import v1_router

BASE_URL = os.environ.get("BASE_URL", "")

api_router = APIRouter()

api_router.include_router(v1_router, prefix="/v1")


@api_router.get("")
async def get():
    return {
        "message": "Hello from the Tracks API!",
        "version 1": f"{BASE_URL}/api/v1",
    }
