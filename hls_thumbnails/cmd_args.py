from argparse import ArgumentParser

defaults = {
    'role_arn':  'arn:aws:iam::611670965994:role/gcc-S3Test',
    'role_session_name': 'brian_test',
    'output_bucket_name': 'hls-global',
    'input_bucket_name': 'hls-global',
    'input_prefix': 'L30/data/',
}


def get_args():
    parser = ArgumentParser()
    for key, value in defaults.items():
        parser.add_argument('--' + key, default=value)
    return parser.parse_args()
