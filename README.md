# hls-thumbnails
Generate thumbnails for HLS.


### Requirements
The use of rasterio for HDF does not allow for the regular pip install of rasterio using wheels. It requires a preinstalled gdal version that supports HDF4 installed on the system and install rasterio using
```
pip install rasterio --no-binary rasterio
```

Installation requires python development libraries and hdf4 binaries. On an Ubuntu/Debian system they can be installed with the following.
```bash
sudo apt-get install build-essential python3-dev python-dev libhdf4-dev # For Python 3

```
### Installation
Install for local testing
```bash
pip install -e .["test"]
```

This will install the `create_thumbnail` executable on the path,
which is used as follows:

```bash
create_thumbnail -i <input_file> -o <output_file> -s <instrument>
```

**Example usage:**

```bash
thumbnail.py -i HLS.L30.T04VER.hdf -o HLS.L30.T04VER.jpeg -s L30
thumbnail.py -i HLS.S30.T04VER.hdf -o HLS.L30.T04VER.jpeg -s S30
```

### Tests
Run Tests on Docker
```bash
docker build -t hls_thumbnails . && docker run hls_thumbnails
```
