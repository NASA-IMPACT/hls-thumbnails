from os import path, listdir
from tempfile import TemporaryDirectory

import pytest
from hls_thumbnails.create_thumbnail import Thumbnail


TEST_PATH = path.dirname(__file__)
TEST_DATA_PATH = path.join(TEST_PATH, "test_data")


def get_dirs(directory):
    for f in listdir(directory):
        filename = path.join(directory, f)
        if path.isdir(filename):
            yield filename


@pytest.mark.parametrize("input_dir", get_dirs(TEST_DATA_PATH))
def test_thumbnails(input_dir):
    with TemporaryDirectory() as tmpdir:
        output_file = path.join(tmpdir, f"{path.basename(input_dir)}.jpeg")
        Thumbnail(input_dir, output_file).prepare()
        assert path.exists(output_file)
