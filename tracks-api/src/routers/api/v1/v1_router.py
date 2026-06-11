"""
API version 1 router. Registers API paths.
module: src/routers/api/v1/v1_router.py
"""

from fastapi import APIRouter


v1_router = APIRouter()


@v1_router.get("")
async def get():
    return {
        "message": "Welcome to version 1 of the Tracks API!",
    }


@v1_router.get("/health")
async def health():
    return {"status": 200, "message": "OK"}
