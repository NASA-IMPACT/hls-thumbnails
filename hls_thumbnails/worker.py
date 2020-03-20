import math
import rasterio
import sys
import logging

import numpy as np
import boto3

from PIL import Image
from pyhdf.SD import SD, SDC
from botocore.exceptions import ClientError

from hls_thumbnails import update_credentials
from hls_thumbnails.config import get_config


# Calculation configurations
HIGH_THRES = 7500
HIGH_VAL = 255.

LOW_VAL = math.e
LOW_THRES = 100

# Instrument based configurations
LANDSAT_BANDS = ['band04', 'band03', 'band02']
LANDSAT_ID = 'L30'

SENTINEL_BANDS = ['B04', 'B03', 'B02']
SENTINEL_ID = 'S30'

# Image configurations
IMG_SIZE = 1000

# for lambda
FILE_LOCATION = "./{}"
THUMBNAIL_LOCATION = FILE_LOCATION.format("thumbnails/{}")


class Browse:

    def __init__(self, file_name, stretch='log'):
        self.file_name = file_name
        self.stretch = stretch
        self.attributes = {}
        self.config = get_config()
        self.define_high_low()
        self.select_constellation()

    def define_high_low(self):
        """
        Public:
            Define High and Low values as thresholds
            based on the stretch type defined by user.
        """
        self.high_thres = HIGH_THRES
        self.low_thres = LOW_THRES
        self.low_value = LOW_VAL
        self.high_thres = math.log(self.high_thres)
        self.low_thres = math.log(self.low_thres)
        self.low_value = LOW_VAL
        self.diff = self.high_thres - self.low_thres

    def select_constellation(self):
        """
        Public:
            Based on file name of the granule it decides
            on which bands to use for image generation
        """
        self.bands = LANDSAT_BANDS
        if SENTINEL_ID in self.file_name:
            self.bands = SENTINEL_BANDS

    def prepare(self):
        """
        Public:
            Handles reprojection of file, conversion of hdf into GeoTIFF
        """
        data_file = SD(self.file_name, SDC.READ)
        extracted_data = list()
        for band in self.bands:
            band_data = data_file.select(band)
            extracted_data.append(band_data.get())
        self.attributes = data_file.attributes()
        data_file.end()
        extracted_data = np.array(extracted_data)
        extracted_data[np.where(extracted_data <= self.low_thres)] \
            = self.low_value
        extracted_data = np.log(extracted_data)
        extracted_data[np.where(extracted_data >= self.high_thres)] = HIGH_VAL
        indices = np.where(
            (extracted_data > self.low_thres)
            & (extracted_data < self.high_thres)
        )
        extracted_data[indices] = (
            HIGH_VAL * (extracted_data[indices] - self.low_thres) / self.diff
        )
        extracted_data = extracted_data.astype(rasterio.uint8)
        file_name = self.file_name.split('/')[-1]
        thumbnail_file_name = self.prepare_thumbnail(extracted_data, file_name)
        return thumbnail_file_name

    def prepare_thumbnail(self, extracted_data, file_name):
        """
        Public:
            Creates thumbnail of the granule
        Args:
            extracted_date - numpy array of the image
            file_name - Name of the file being opened
        """
        thumbnail_file_name = file_name.replace('.hdf', '.jpeg')
        extracted_data = np.rollaxis(extracted_data, 0, 3)
        img = Image.fromarray(extracted_data)
        img = img.resize((IMG_SIZE, IMG_SIZE))
        img.save(thumbnail_file_name)
        self.move_to_S3(self.config['output_bucket_name'], thumbnail_file_name)
        return thumbnail_file_name

    def move_to_S3(self, bucket_name, report_name):
        """
        If the metadata file is able to be successfully written by the
        processing code, we move the data to S3 using the assumed role
        from GCC. This is required for the bucket access policy to be
        applied correctly such that LPDAAC has read/get access.
        """
        product = report_name.split(".")[1]
        object_name = "/".join([product, "thumbnail", report_name])
        creds = update_credentials.assume_role(
            self.config['role_arn'], self.config['role_session_name']
        )
        client = boto3.client(
            "s3",
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"],
        )
        try:
            client.upload_file(report_name, bucket_name, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True


if __name__ == "__main__":
    file_name = sys.argv[1]
    browse = Browse(file_name, stretch='log')
    thumbnail_file_name = browse.prepare()
