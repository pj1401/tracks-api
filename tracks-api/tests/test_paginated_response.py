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
            "year": 1987,
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
        {
            "id": 41,
            "href": "http://example-domain.com/tracks-api/api/v1/tracks/41",
            "created_at": "2026-06-16T13:45:35.877848Z",
            "updated_at": "2026-06-16T13:45:35.877848Z",
            "name": "Paranoid",
            "total_playcount": 0,
            "spotify_id": "01dw6mDc9xJMoEPasHaV7Y",
            "tags": '"rock, metal, classic_rock, hard_rock, heavy_metal, 70s"',
            "genre": "NaN",
            "year": 1970,
            "duration_ms": 166546,
            "danceability": 0.413,
            "mode": 0,
            "valence": 0.492,
            "artists": [
                {
                    "id": 25,
                    "href": "http://example-domain.com/tracks-api/api/v1/artists/25",
                }
            ],
            "albums": [
                {
                    "id": 40,
                    "href": "http://example-domain.com/tracks-api/api/v1/albums/40",
                }
            ],
        },
    ]


@pytest.fixture
def query_params() -> TrackQueryParams:
    return TrackQueryParams(limit=5, offset=5, tags="metal")  # type: ignore[reportCallIssue]


class TestBuildUrl:
    """
    Tests the _build_url method.
    """

    def test_returns_correct_href(
        self, query_params: TrackQueryParams, data: list[Dict[str, Any]]
    ):
        expected_href = "http://example-domain.com/tracks-api/api/v1/tracks?limit=5&offset=5&sort=id&tags=metal"
        paginated_response = PaginatedResponse(
            "http://example-domain.com",
            "/tracks-api/api/v1/tracks",
            query_params,
            200,
            data,
        )
        actual_href = paginated_response._build_url(query_params.offset)  # type: ignore[reportPrivateUsage]
        assert actual_href == expected_href

    def test_returns_correct_next_url(
        self, query_params: TrackQueryParams, data: list[Dict[str, Any]]
    ):
        expected_next = "http://example-domain.com/tracks-api/api/v1/tracks?limit=5&offset=10&sort=id&tags=metal"
        paginated_response = PaginatedResponse(
            "http://example-domain.com",
            "/tracks-api/api/v1/tracks",
            query_params,
            200,
            data,
        )
        offset = query_params.offset
        limit = query_params.limit
        actual_next = paginated_response._build_url(offset + limit)  # type: ignore[reportPrivateUsage]
        assert actual_next == expected_next

    def test_returns_correct_previous_url(
        self, query_params: TrackQueryParams, data: list[Dict[str, Any]]
    ):
        expected_previous = "http://example-domain.com/tracks-api/api/v1/tracks?limit=5&offset=0&sort=id&tags=metal"
        paginated_response = PaginatedResponse(
            "http://example-domain.com",
            "/tracks-api/api/v1/tracks",
            query_params,
            200,
            data,
        )
        offset = query_params.offset
        limit = query_params.limit
        actual_previous = paginated_response._build_url(max(offset - limit, 0))  # type: ignore[reportPrivateUsage]
        assert actual_previous == expected_previous


class TestToDict:
    """
    Tests the to_dict method.
    """

    def test_data_length_less_than_limit(
        self, query_params: TrackQueryParams, data: list[Dict[str, Any]]
    ):
        """
        There should be no next URL when the number of returned records is less than limit.
        """
        expected_href = "http://example-domain.com/tracks-api/api/v1/tracks?limit=5&offset=5&sort=id&tags=metal"
        expected_next = None
        expected_previous = "http://example-domain.com/tracks-api/api/v1/tracks?limit=5&offset=0&sort=id&tags=metal"
        paginated_response = PaginatedResponse(
            "http://example-domain.com",
            "/tracks-api/api/v1/tracks",
            query_params,
            200,
            data,
        )
        response_dict = paginated_response.to_dict()
        assert response_dict["href"] == expected_href
        assert response_dict["next"] == expected_next
        assert response_dict["previous"] == expected_previous

    def test_data_length_equals_limit(
        self, query_params: TrackQueryParams, data: list[Dict[str, Any]]
    ):
        expected_href = "http://example-domain.com/tracks-api/api/v1/tracks?limit=3&offset=5&sort=id&tags=metal"
        expected_next = "http://example-domain.com/tracks-api/api/v1/tracks?limit=3&offset=8&sort=id&tags=metal"
        expected_previous = "http://example-domain.com/tracks-api/api/v1/tracks?limit=3&offset=2&sort=id&tags=metal"

        # Set limit to the length of the data array.
        query_params.limit = len(data)

        paginated_response = PaginatedResponse(
            "http://example-domain.com",
            "/tracks-api/api/v1/tracks",
            query_params,
            200,
            data,
        )
        response_dict = paginated_response.to_dict()
        assert response_dict["href"] == expected_href
        assert response_dict["next"] == expected_next
        assert response_dict["previous"] == expected_previous

    def test_offset_is_zero(
        self, query_params: TrackQueryParams, data: list[Dict[str, Any]]
    ):
        """
        No previous URL is returned when offset is 0.
        """
        expected_href = "http://example-domain.com/tracks-api/api/v1/tracks?limit=5&offset=0&sort=id&tags=metal"
        expected_next = None
        expected_previous = None

        # Set offset to 0 for this test.
        query_params.offset = 0

        paginated_response = PaginatedResponse(
            "http://example-domain.com",
            "/tracks-api/api/v1/tracks",
            query_params,
            200,
            data,
        )
        response_dict = paginated_response.to_dict()
        assert response_dict["href"] == expected_href
        assert response_dict["next"] == expected_next
        assert response_dict["previous"] == expected_previous

    def test_default_values_included_in_url(self, data: list[Dict[str, Any]]):
        """
        Default values for limit, offset and id query parameters
          should be included when they aren't specified.
        """
        expected_href = "http://example-domain.com/tracks-api/api/v1/tracks?limit=20&offset=0&sort=id&tags=metal"
        expected_next = None
        expected_previous = None
        paginated_response = PaginatedResponse(
            "http://example-domain.com",
            "/tracks-api/api/v1/tracks",
            TrackQueryParams(tags="metal"),  # type: ignore[reportCallIssue]
            200,
            data,
        )
        response_dict = paginated_response.to_dict()
        assert response_dict["href"] == expected_href
        assert response_dict["next"] == expected_next
        assert response_dict["previous"] == expected_previous
