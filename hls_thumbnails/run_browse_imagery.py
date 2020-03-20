import os
import gc
import boto3

from hls_thumbnails import update_credentials
from hls_thumbnails.worker import Browse
from hls_thumbnails.config import get_config


def create_dir(directory):
    try:
        os.makedirs(directory)
    except Exception:
        pass

# bucket_name = name of the bucket where the hdf files are located
# profile_name = aws profile name.


def download_and_create(bucket_name, prefix=''):
    # Make sure the download path exists.
    create_dir(prefix)

    config = get_config()
    creds = update_credentials.assume_role(
        config['role_arn'], config['role_session_name']
    )
    s3 = boto3.resource(
        's3',
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )
    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key == prefix or obj.key.endswith('.hdr'):
            continue
        file_name = './' + obj.key
        print(file_name)
        # splits = obj.key.split('.')[1:4]
        print('Downloading File', file_name)
        print(obj.key, file_name)
        bucket.download_file(obj.key, file_name)
        print('Download Done!')
        # header_file_name = file_name

        if '.hdf.hdr' in file_name:
            continue
        print(file_name)
        if os.path.exists(file_name):
            print("running for:", file_name)
            browse = Browse(file_name, stretch='log')
            thumbnail_name = browse.prepare()
            del(browse)
            print("Done:", thumbnail_name)
            os.remove(file_name)
            os.remove(thumbnail_name)
            print("Removed:", file_name)
        print('====================')
        gc.collect()


def run_browse_imagery():
    config = get_config()
    # download l30 data and create merged geotiffs.
    download_and_create(config['l30_bucket_name'], prefix=config['l30_prefix'])
    # download s30 data and create merged geotiffs.
    download_and_create(config['s30_bucket_name'], prefix=config['s30_prefix'])


if __name__ == '__main__':
    run_browse_imagery()
