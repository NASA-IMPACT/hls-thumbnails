from os import path, listdir
from tempfile import TemporaryDirectory

import pytest
from hls_thumbnails.create_thumbnail import Thumbnail


TEST_PATH = path.dirname(__file__)
TEST_DATA_PATH = path.join(TEST_PATH, "test_data")


def get_files(directory):
    for f in listdir(directory):
        filename = path.join(directory, f)
        if path.isfile(filename):
            yield filename


@pytest.mark.parametrize("input_file", get_files(TEST_DATA_PATH))
def test_thumbnails(input_file):
    with TemporaryDirectory() as tmpdir:
        output_file = path.join(tmpdir, "test.jpeg")
        Thumbnail(input_file, output_file).prepare()
        assert path.exists(output_file)
