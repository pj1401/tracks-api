"""
Defines user routes.
module: src/blueprints/api/v1/users/routes.py
"""

from flask import Blueprint, g
from src.decorators.auth_required import auth_required
from models import User
from src.util.schemas.user import UserModel
from src.controllers.user_controller import UserController
from src.repositories.user_repo import UserRepository
from src.services.user_service import UserService

users_bp = Blueprint("users", __name__)


@users_bp.before_request
def before_request():
    """Create objects once per request."""
    g.user_repo = UserRepository(g.db_manager, User, g.base_url)
    g.user_service = UserService(g.user_repo, UserModel)
    g.user_controller = UserController(g.user_service)


@users_bp.route("/<int:id>", methods=["DELETE"])
@auth_required()
def delete(id: int):
    return g.user_controller.delete(id)
