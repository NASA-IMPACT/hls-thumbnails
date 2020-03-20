from moto import mock_s3
from pytest import fixture
from boto3 import resource as boto_resource
from os import environ, path, listdir
from hls_thumbnails.run_browse_imagery import download_and_create


S3_TEST_BUCKET_NAME = 'test-bucket'
TEST_PATH = path.dirname(__file__)
TEST_DATA_PATH = path.join(TEST_PATH, 'test_data')
L30_TEST_DATA_PATH = path.join(TEST_DATA_PATH, 'l30')
S30_TEST_DATA_PATH = path.join(TEST_DATA_PATH, 's30')


class TestArgs:
    role_arn = ''
    role_session_name = ''
    output_bucket_name = S3_TEST_BUCKET_NAME
    input_bucket_name = S3_TEST_BUCKET_NAME
    input_prefix = ''


@fixture(scope='class')
def mock_environment():
    env = {
        # Prevent from mutating real AWS infrastructure
        'AWS_ACCESS_KEY_ID': 'testing',
        'AWS_SECRET_ACCESS_KEY': 'testing',
    }
    old_environ = environ.copy()
    environ.update(env)

    yield environ

    environ.clear()
    environ.update(old_environ)


def get_files(directory):
    for f in listdir(directory):
        filename = path.join(directory, f)
        if path.isfile(filename):
            yield filename, f


@fixture(scope='class')
def s3_test_bucket(mock_environment):
    with mock_s3():
        bucket = boto_resource('s3').create_bucket(Bucket=S3_TEST_BUCKET_NAME)
        for file_path, name in get_files(L30_TEST_DATA_PATH):
            bucket.upload_file(file_path, 'L30/data/' + name)
        for file_path, name in get_files(S30_TEST_DATA_PATH):
            bucket.upload_file(file_path, 'S30/data/' + name)
        yield bucket


class TestThumbnails:
    def test_thumbnails(self, mock_environment, s3_test_bucket):
        # Run for L30.
        l30_args = TestArgs()
        l30_args.input_prefix = 'L30/data/'
        download_and_create(l30_args)

        # Run for S30.
        s30_args = TestArgs()
        s30_args.input_prefix = 'S30/data/'
        download_and_create(s30_args)

        # We should have jpeg files as thumbnails in the bucket
        # for each hd5 file.

        jpeg_files = [
            o.key
            for o in s3_test_bucket.objects.all()
            if o.key.endswith('.jpeg')
        ]
        # Check that L30 thumbnails are created.
        for file_path, name in get_files(L30_TEST_DATA_PATH):
            if name.endswith('.hdf'):
                key = 'L30/thumbnail/' + name.replace('.hdf', '.jpeg')
                assert key in jpeg_files
        # Check that S30 thumbnails are created.
        for file_path, name in get_files(S30_TEST_DATA_PATH):
            if name.endswith('.hdf'):
                key = 'S30/thumbnail/' + name.replace('.hdf', '.jpeg')
                assert key in jpeg_files
