# hls-thumbnails

Generate thumbnails for HLS.

## Installation

Make sure you have python development libraries and hdf4 binaries installed
in your system.

You can then install this application with `pip`:

```bash
pip install .
```

This will install the `run-browse-imagery` as an executable on the path.
The command line supports the following arguments.

| Argument | Default Value | Use |
| --- | --- | --- |
| role_arn | `arn:aws:iam::611670965994:role/gcc-S3Test` | AWS Role ARN |
| role_session_name | `brian_test` | AWS Role Session Name |
| input_bucket_name | `hls-global` | S3 Bucket containing input HD5 files |
| input_prefix | `L30/data/` | S3 key prefix to filter the input files |
| output_bucket_name | `hls-global` | S3 Bucket to store output thumbnails |

#### Example Usage

```bash
# Run with default arguments for L30
run-browse-imagery --input_prefix='L30/data/'
# Run with default arguments for S30
run-browse-imagery --input_prefix='S30/data/'

# Run with custom arguments:
run-browse-imagery \
    --input_bucket_name="l30-sample" \
    --input_prefix= \
    --role_arn= \
    --role_session_name= \
    --output_bucket_name="hls-test-thumbnails"
```


## Testing

Run `pytest` to test the application. S3 buckets are mocked and locally stored
data are used for testing.

```bash
pytest
```
