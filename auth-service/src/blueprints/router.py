"""
The main router that registers the routes.
module: src/blueprints/router.py
"""

from flask import Blueprint
from src.blueprints.api.router import router_api_bp

router_bp = Blueprint("/", __name__)
router_bp.register_blueprint(router_api_bp, url_prefix="/api")
