"""
Version 1 sub API application.
module: src.apis.api_v1
"""

from fastapi import FastAPI
from ..routers.api.v1.v1_router import v1_router

api_v1 = FastAPI()

api_v1.include_router(v1_router)
