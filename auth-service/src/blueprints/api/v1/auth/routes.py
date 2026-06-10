"""
Defines auth routes.
module: src/blueprints/api/v1/auth/routes.py
"""

from flask import Blueprint, g
from models import User
from src.util.schemas.user import UserModel
from src.controllers.user_controller import UserController
from src.repositories.user_repo import UserRepository
from src.services.user_service import UserService

auth_bp = Blueprint("auth", __name__)


@auth_bp.before_request
def before_request():
    """Create objects once per request."""
    g.user_repo = UserRepository(g.db_manager, User, g.base_url)
    g.user_service = UserService(g.user_repo, UserModel)
    g.user_controller = UserController(g.user_service)


@auth_bp.route("/register", methods=["POST"])
def create_user():
    return g.user_controller.create_user()


@auth_bp.route("/login", methods=["POST"])
def login_user():
    return g.user_controller.login()
