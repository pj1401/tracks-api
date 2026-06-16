"""
Version 1 sub API application.
module: src.apis.v1_api
"""

from fastapi import FastAPI
from src.decorators.exception_handlers import setup_exception_handlers
from ..routers.api.v1.v1_router import v1_router

api_v1 = FastAPI(title="Tracks API v1", version="0.2.0")

api_v1.include_router(v1_router)

setup_exception_handlers(api_v1)
