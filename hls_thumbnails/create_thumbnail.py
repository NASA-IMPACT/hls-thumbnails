#!/usr/bin/env python
import math
import os
import sys
import getopt
import numpy as np
import rasterio
from PIL import Image


# Calculation configurations
HIGH_THRES = 7500
HIGH_VAL = 255.0

LOW_VAL = math.e
LOW_THRES = 100

# Instrument based configurations
SENTINEL_ID = "S30"
LANDSAT_ID = "L30"
BANDS = {
    SENTINEL_ID: ["B04", "B03", "B02"],
    LANDSAT_ID: ["B04", "B03", "B02"],
}

# Image configurations
IMG_SIZE = 1000


def find_band_tif(tifs, band):
    """
    Find the tif file for the given band.

    Args:
        tifs - list of tif files
        band - band name
    """
    for tif in tifs:
        if band in tif:
            return tif

    raise ValueError(f"Missing tif for band {band}")


class Thumbnail:
    def __init__(self, input_dir, output_file, instrument=None, stretch="log"):
        self.input_dir = input_dir
        self.output_file = output_file
        self.instrument = instrument
        self.stretch = stretch
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
            Decides on which bands to use for image generation.
            If instrument is not provided, decide base on filename.
        """
        tifs = [
            os.path.join(self.input_dir, filename)
            for filename in os.listdir(self.input_dir)
            if filename.endswith(".tif")
        ]

        if self.instrument is None:
            self.instrument = (
                SENTINEL_ID
                if any(SENTINEL_ID in tif for tif in tifs)
                else LANDSAT_ID
            )

        self.bands = BANDS[self.instrument]
        self.band_tifs = [find_band_tif(tifs, band) for band in self.bands]

    def prepare(self):
        """
        Public:
            Handles reprojection of file, conversion of hdf into GeoTIFF
        """
        extracted_data = []

        for tif in self.band_tifs:
            with rasterio.open(tif) as src:
                band_data = src.read(1)

            extracted_data.append(band_data)

        extracted_data = np.array(extracted_data)
        extracted_data[np.where(extracted_data <= self.low_thres)] = self.low_value
        extracted_data = np.log(extracted_data)  # pyright: ignore[reportAttributeAccessIssue] # noqa: E501
        extracted_data[np.where(extracted_data >= self.high_thres)] = HIGH_VAL
        indices = np.where(
            (extracted_data > self.low_thres) & (extracted_data < self.high_thres)
        )
        extracted_data[indices] = (
            HIGH_VAL * (extracted_data[indices] - self.low_thres) / self.diff
        )
        extracted_data = extracted_data.astype(rasterio.uint8)

        self.prepare_thumbnail(extracted_data)

    def prepare_thumbnail(self, extracted_data):
        """
        Public:
            Creates thumbnail of the granule
        Args:
            extracted_data - numpy array of the image
        """
        extracted_data = np.rollaxis(extracted_data, 0, 3)
        img = Image.fromarray(extracted_data)
        img = img.resize((IMG_SIZE, IMG_SIZE))
        img.save(self.output_file)


SHORT_OPTIONS = "i:o:s:"
LONG_OPTIONS = ["inputdir=", "outputfile=", "instrument="]
HELP_TEXT = "create_thumbnail -i <input_dir> -o <output_file> -s [L30|S30]"


def create_thumbnail():
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, SHORT_OPTIONS, LONG_OPTIONS)
    except getopt.GetoptError:
        print(HELP_TEXT)
        sys.exit(2)

    input_dir, output_file, instrument = None, None, None

    for opt, arg in opts:
        if opt in ("-i", "--inputdir"):
            input_dir = arg
        elif opt in ("-o", "--outputfile"):
            output_file = arg
        elif opt in ("-s", "--instrument"):
            instrument = arg

    if input_dir is None or output_file is None:
        print(HELP_TEXT)
        sys.exit(2)

    if instrument not in [LANDSAT_ID, SENTINEL_ID]:
        print("Invalid instrument: ", instrument)
        sys.exit(2)

    Thumbnail(input_dir, output_file, instrument).prepare()


if __name__ == "__main__":
    create_thumbnail()
