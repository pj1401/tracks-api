"""
API version 1 router. Registers API endpoints.
module: src/blueprints/api/v1/router.py
"""

from typing import cast
from flask import Blueprint, jsonify, current_app
from .auth.routes import auth_bp
from .docs.routes import docs_bp
from .users.routes import users_bp

router_v1_bp = Blueprint("/", __name__)
router_v1_bp.register_blueprint(auth_bp, url_prefix="/auth")
router_v1_bp.register_blueprint(docs_bp, url_prefix="/docs")
router_v1_bp.register_blueprint(users_bp, url_prefix="/users")


@router_v1_bp.route("/", methods=["GET"])
def get():
    base_url = cast(str, current_app.config["BASE_URL"])
    response = {
        "message": "Welcome to version 1 of Auth API!",
        "docs": f"{base_url}/api/v1/docs",
    }
    return jsonify(response)


@router_v1_bp.route("/health", methods=["GET"])
def health():
    response: dict[str, int | str] = {"status": 200, "message": "OK"}
    return jsonify(response)
