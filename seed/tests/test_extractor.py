import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.extractor import read_hdf5_data


@pytest.fixture
def mock_hdf5() -> MagicMock:
    """
    Get a mock hdf5 file.

    :return: A mock of the hdf5 file
    :rtype: MagicMock
    """
    analysis_dtype = np.dtype([("track_id", "S18")])
    metadata_dtype = np.dtype(
        [
            ("release", "S100"),
            ("release_7digitalid", np.int32),
        ]
    )

    analysis_rows = np.array(
        [(b"TRMZXEW128F9341FD5",), (b"TRIOREW128F424EAF0",)],
        dtype=analysis_dtype,
    )
    metadata_rows = np.array(
        [(b"Live Lounge", 557045), (b"Real album name", 641023)],
        dtype=metadata_dtype,
    )

    analysis_songs = MagicMock()
    analysis_songs.__iter__ = MagicMock(return_value=iter(analysis_rows))

    metadata_songs = MagicMock()
    metadata_songs.__iter__ = MagicMock(return_value=iter(metadata_rows))

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
