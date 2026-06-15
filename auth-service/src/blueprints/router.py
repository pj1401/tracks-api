"""
The main router that registers the routes.
module: src/blueprints/router.py
"""

from flask import Blueprint, redirect, url_for
from src.blueprints.api.router import router_api_bp

router_bp = Blueprint("/", __name__)
router_bp.register_blueprint(router_api_bp, url_prefix="/api")


@router_bp.route("/", methods=["GET"])
def get():
    return redirect(url_for(".api.get"))
