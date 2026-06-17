"""
Load a static openapi.json file.
module: src.dependencies.static_openapi
"""

import json
from typing import Any, Callable
from fastapi import FastAPI
from pathlib import Path


def static_openapi_loader(app: FastAPI, path: str) -> Callable[[], dict[str, Any]]:
    """
    Build a callable that sets the openapi.json to a static file.
    """

    def load_static_openapi() -> dict[str, Any]:
        """
        Set the openapi.json to a static file.
        """
        if app.openapi_schema is None:
            loaded: dict[str, Any] = json.loads(Path(path).read_text())
            app.openapi_schema = loaded
        return app.openapi_schema

    return load_static_openapi
