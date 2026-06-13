import pytest
import os
from dotenv import load_dotenv
from src.extractor import read_hdf5_data  # type: ignore

load_dotenv()

HDF5_PATH = os.getenv("HDF5_PATH")


@pytest.fixture
def hdf5_path() -> str | None:
    return HDF5_PATH


class TestReadHdf5Data:
    """
    Test the read_hdf5_data function.
    """

    def test_correct_dict_keys(self, hdf5_path: str):
        hdf5_lookup = read_hdf5_data(hdf5_path)
        assert isinstance(hdf5_lookup, dict)
        assert "album_name" in list(hdf5_lookup.values())[0]
        assert "old_album_id" in list(hdf5_lookup.values())[0]
