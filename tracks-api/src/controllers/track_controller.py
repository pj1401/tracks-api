"""
The TrackController class.
module: src/controllers/track_controller.py
"""

from src.controllers.writable_controller import WritableController
from src.services.track_service import TrackService


class TrackController(WritableController[TrackService]):
    """
    HTTP layer for the tacks collection.
    """

    def __init__(self, track_service: TrackService, base_url: str, path: str):
        super().__init__(track_service, base_url, path)
