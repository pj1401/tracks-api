"""
The AlbumController class.
module: src/controllers/album_controller.py
"""

from src.controllers.base_controller import BaseController
from src.services.album_service import AlbumService


class AlbumController(BaseController[AlbumService]):
    """
    AlbumController for handling read endpoints.
    """

    def __init__(self, album_service: AlbumService, base_url: str, path: str):
        super().__init__(album_service, base_url, path)
