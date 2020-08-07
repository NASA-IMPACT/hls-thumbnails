from os import path, listdir, remove
from hls_thumbnails.create_thumbnail import Thumbnail


TEST_PATH = path.dirname(__file__)
TEST_DATA_PATH = path.join(TEST_PATH, "test_data")


def get_files(directory):
    for f in listdir(directory):
        filename = path.join(directory, f)
        if path.isfile(filename):
            yield filename


class TestThumbnails:
    def test_thumbnails(self):
        for f in get_files(TEST_DATA_PATH):
            Thumbnail(f, "test.jpeg").prepare()
            assert path.exists("test.jpeg")
            remove("test.jpeg")
