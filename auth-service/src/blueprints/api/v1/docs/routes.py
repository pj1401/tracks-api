"""
Defines the docs route.
module: src/blueprints/api/v1/docs/routes.py
"""

import os
from flask_swagger_ui import get_swaggerui_blueprint  # type: ignore

PATH_PREFIX = os.environ.get("PATH_PREFIX", "")
SWAGGER_URL = f"{PATH_PREFIX}/api/v1/docs"
API_URL = f"{PATH_PREFIX}/static/auth-api-v1.openapi.json"
docs_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Auth API v1",
        "docExpansion": "none",
        "persistAuthorization": True,
        "validatorUrl": "none",
    },
)
