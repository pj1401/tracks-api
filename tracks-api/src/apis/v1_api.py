"""
Version 1 sub API application.
module: src.apis.v1_api
"""

from typing import Any

from fastapi import FastAPI
from src.decorators.exception_handlers import setup_exception_handlers
from ..routers.api.v1.v1_router import v1_router
import json
from pathlib import Path


def load_static_openapi() -> dict[str, Any]:
    if not api_v1.openapi_schema:
        api_v1.openapi_schema = json.loads(
            Path("static/tracks-api-v1.openapi.json").read_text()
        )
    return api_v1.openapi_schema


api_v1 = FastAPI(title="Tracks API v1", version="0.3.0")

api_v1.openapi = load_static_openapi

api_v1.include_router(v1_router)

setup_exception_handlers(api_v1)
