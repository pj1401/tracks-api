"""
The ArtistController class.
module: src/controllers/artist_controller.py
"""

from src.controllers.base_controller import BaseController
from src.services.artist_service import ArtistService


class ArtistController(BaseController[ArtistService]):
    """
    ArtistController for handling read endpoints.
    """

    def __init__(self, artist_service: ArtistService, base_url: str, path: str):
        super().__init__(artist_service, base_url, path)
