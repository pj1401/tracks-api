"""
The router that registers the api routes.
module: src/blueprints/api/router.py
"""

from typing import cast
from flask import Blueprint, jsonify, g, current_app, url_for
from src.blueprints.api.v1.router import router_v1_bp

router_api_bp = Blueprint("api", __name__)
router_api_bp.register_blueprint(router_v1_bp, url_prefix="/v1")


@router_api_bp.before_request
def before_request():
    """Create objects once per request."""
    g.base_url = cast(str, current_app.config["BASE_URL"])


@router_api_bp.route("/", methods=["GET"])
def get():
    base_url = cast(str, current_app.config["BASE_URL"])
    response = {
        "message": "Welcome to Auth API!",
        "version 1": f"{base_url}{url_for('.v1.get')}",
    }
    return jsonify(response)
