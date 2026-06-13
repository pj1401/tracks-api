import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.extractor import read_hdf5_data


@pytest.fixture
def mock_hdf5() -> MagicMock:
    analysis_songs = MagicMock()
    analysis_songs.__getitem__ = MagicMock(
        side_effect=lambda key: {
            "track_id": np.array([b"TRMZXEW128F9341FD5", b"TRIOREW128F424EAF0"]),
        }[key]
    )

    metadata_songs = MagicMock()
    metadata_songs.__getitem__ = MagicMock(
        side_effect=lambda key: {
            "release": np.array([b"Live Lounge", b"Real album name"]),
            "release_7digitalid": np.array([557045, 641023]),
        }[key]
    )

    mock_file = MagicMock()
    mock_file.__enter__ = lambda s: s
    mock_file.__exit__ = MagicMock(return_value=False)
    mock_file.__getitem__.side_effect = lambda key: {
        "analysis": {"songs": analysis_songs},
        "metadata": {"songs": metadata_songs},
    }[key]

    return mock_file


class TestReadHdf5Data:
    """
    Test the read_hdf5_data function.
    """

    def test_correct_dict_keys(self, mock_hdf5: MagicMock):
        with patch("src.extractor.h5py.File", return_value=mock_hdf5):
            result = read_hdf5_data("fake/path.h5")

        assert isinstance(result, dict)
        key = "TRMZXEW128F9341FD5"
        assert key in result
        assert "album_name" in result[key]
        assert "old_album_id" in result[key]

    def test_correct_values(self, mock_hdf5: MagicMock):
        with patch("src.extractor.h5py.File", return_value=mock_hdf5):
            result = read_hdf5_data("fake/path.h5")

        assert result["TRMZXEW128F9341FD5"]["album_name"] == "Live Lounge"
        assert result["TRMZXEW128F9341FD5"]["old_album_id"] == "557045"
