from os import environ


defaults = {
    'role_arn':  'arn:aws:iam::611670965994:role/gcc-S3Test',
    'role_session_name': 'brian_test',
    'output_bucket_name': 'hls-global',
    'l30_bucket_name': 'hls-global',
    's30_bucket_name': 'hls-global',
    'l30_prefix': 'L30/data/',
    's30_prefix': 'S30/data/',
}


def get_config():
    return {
        key: environ.get(key, value)
        for key, value in defaults.items()
    }
