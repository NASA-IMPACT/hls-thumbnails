#!/usr/bin/env python
import math
import sys
import getopt
import numpy as np
import rasterio
from PIL import Image
from pyhdf.SD import SD, SDC


# Calculation configurations
LOW_VAL = 1
HIGH_VAL = 255

LOW_THRES = 100
HIGH_THRES = 7500
# Instrument based configurations
SENTINEL_ID = "S30"
LANDSAT_ID = "L30"
BANDS = {
    SENTINEL_ID: ["B04", "B03", "B02"],
    LANDSAT_ID: ["B04", "B03", "B02"],
}

# Image configurations
IMG_SIZE = 1000


class Thumbnail:
    def __init__(self, input_file, output_file, instrument=None, stretch="log"):
        self.input_file = input_file
        self.output_file = output_file
        self.instrument = instrument
        self.stretch = stretch
        self.attributes = {}
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
        self.high_thres = np.log(self.high_thres)
        self.low_thres = np.log(self.low_thres)
        self.diff = self.high_thres - self.low_thres

    def select_constellation(self):
        """
        Public:
            Decides on which bands to use for image generation.
            If instrument is not provided, decide base on filename.
        """
        if self.instrument is None:
            if SENTINEL_ID in self.input_file:
                self.instrument = SENTINEL_ID
            else:
                self.instrument = LANDSAT_ID
        self.bands = BANDS[self.instrument]

    def prepare(self):
        """
        Public:
            Handles reprojection of file, conversion of hdf into GeoTIFF
        """
        data_file = SD(self.input_file, SDC.READ)
        extracted_data = list()
        for band in self.bands:
            band_data = data_file.select(band)
            '''
            data = band_data.get()
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    if data[i,j] == -9999:
                        pass
                    elif data[i,j] <= math.e**self.low_thres:
                        data[i,j] = LOW_VAL
                    elif data[i,j] >= math.e**self.high_thres:
                        data[i,j] = HIGH_VAL
                    else:
                        data[i,j] = HIGH_VAL* (np.log(data[i,j]) - self.low_thres) / self.diff
            extracted_data.append(data)
            '''
            extracted_data.append(band_data.get())
        self.attributes = data_file.attributes()
        data_file.end()
        extracted_data = np.array(extracted_data)
        output_data = np.empty(extracted_data.shape)
        indices = np.where(
            (extracted_data > LOW_THRES) & (extracted_data < HIGH_THRES)
        )
        output_data[indices] = (
            HIGH_VAL * (np.ma.log(extracted_data[indices]) - self.low_thres) / self.diff
        )
        output_data[np.where(extracted_data <= LOW_THRES)] = LOW_VAL
       # output_data[np.where(extracted_data == -9999)] = HIGH_VAL
        output_data[np.where((extracted_data >= HIGH_THRES) | (extracted_data == -9999))] = HIGH_VAL
        output_data = output_data.astype(rasterio.uint8)
        file_name = self.input_file.split("/")[-1]
        self.prepare_thumbnail(output_data, file_name)

    def prepare_thumbnail(self, extracted_data, file_name):
        """
        Public:
            Creates thumbnail of the granule
        Args:
            output_data - numpy array of the image
            file_name - Name of the file being opened
        """
        extracted_data = np.rollaxis(extracted_data, 0, 3)
        img = Image.fromarray(extracted_data)
        img = img.resize((IMG_SIZE, IMG_SIZE))
        img.save(self.output_file)


SHORT_OPTIONS = "i:o:s:"
LONG_OPTIONS = ["inputfile=", "outputfile=", "instrument="]
HELP_TEXT = "create_thumbnail -i <input_file> -o <output_file> -s [L30|S30]"


def create_thumbnail():
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, SHORT_OPTIONS, LONG_OPTIONS)
    except getopt.GetoptError:
        print(HELP_TEXT)
        sys.exit(2)

    input_file, output_file, instrument = None, None, None
    for opt, arg in opts:
        if opt in ("-i", "--inputfile"):
            input_file = arg
        elif opt in ("-o", "--outputfile"):
            output_file = arg
        elif opt in ("-s", "--instrument"):
            instrument = arg

    if input_file is None or output_file is None:
        print(HELP_TEXT)
        sys.exit(2)

    if instrument not in [LANDSAT_ID, SENTINEL_ID]:
        print("Invalid instrument: " + instrument)
        sys.exit(2)

    Thumbnail(input_file, output_file, instrument).prepare()


if __name__ == "__main__":
    create_thumbnail()
