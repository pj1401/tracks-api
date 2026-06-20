"""
Version 1 sub API application.
module: src.apis.v1_api
"""

from fastapi import FastAPI
from src.decorators.exception_handlers import setup_exception_handlers
from src.dependencies.static_openapi import static_openapi_loader
from ..routers.api.v1.v1_router import v1_router

api_v1 = FastAPI(title="Tracks API v1", version="1.0.0")

api_v1.openapi = static_openapi_loader(api_v1, "static/tracks-api-v1.openapi.json")

api_v1.include_router(v1_router)

setup_exception_handlers(api_v1)
