"""
Tests for the PaginatedResponse class.
module: tests.test_paginated_response
"""

import pytest
from typing import Any, Dict
from models.schemas.tracks import TrackQueryParams
from src.util.paginated_response import PaginatedResponse


@pytest.fixture
def data() -> list[Dict[str, Any]]:
    return [
        {
            "id": 30,
            "href": "http://example-domain.com/tracks-api/api/v1/tracks/30",
            "created_at": "2026-06-16T13:45:35.877848Z",
            "updated_at": "2026-06-16T13:45:35.877848Z",
            "name": "Numb",
            "total_playcount": 19,
            "spotify_id": "0kO3njY9N1Rxgv27Ha1lLh",
            "tags": '"rock, alternative, metal, alternative_rock, nu_metal"',
            "genre": "NaN",
            "year": 2003,
            "duration_ms": 185586,
            "danceability": 0.496,
            "mode": 1,
            "valence": 0.243,
            "artists": [
                {
                    "id": 12,
                    "href": "http://example-domain.com/tracks-api/api/v1/artists/12",
                }
            ],
            "albums": [
                {
                    "id": 29,
                    "href": "http://example-domain.com/tracks-api/api/v1/albums/29",
                }
            ],
        },
        {
            "id": 34,
            "href": "http://example-domain.com/tracks-api/api/v1/tracks/34",
            "created_at": "2026-06-16T13:45:35.877848Z",
            "updated_at": "2026-06-16T13:45:35.877848Z",
            "name": "Welcome to the Jungle",
            "total_playcount": 0,
            "spotify_id": "0Aau2Ju1RoLAhL90zRcDx4",
            "tags": '"rock, metal, classic_rock, hard_rock, 80s, heavy_metal"',
            "genre": "NaN",
            "year": 2014,
            "duration_ms": 377386,
            "danceability": 0.272,
            "mode": 1,
            "valence": 0.154,
            "artists": [
                {
                    "id": 21,
                    "href": "http://example-domain.com/tracks-api/api/v1/artists/21",
                }
            ],
            "albums": [
                {
                    "id": 33,
                    "href": "http://example-domain.com/tracks-api/api/v1/albums/33",
                }
            ],
        },
    ]


@pytest.fixture
def query_params() -> TrackQueryParams:
    return TrackQueryParams(limit=5, offset=5, tags="metal")  # type: ignore[reportCallIssue]


class TestBuildUrl:
    """Tests the _build_url method."""

    def test_returns_correct_href(
        self, query_params: TrackQueryParams, data: list[Dict[str, Any]]
    ):
        expected_href = "http://example-domain.com/tracks-api/api/v1/tracks?limit=5&offset=5&tags=metal"
        paginated_response = PaginatedResponse(
            "http://example-domain.com",
            "/tracks-api/api/v1/tracks",
            query_params,
            200,
            data,
        )
        actual_href = paginated_response._build_url(query_params.offset)  # type: ignore[reportPrivateUsage]
        assert actual_href == expected_href
