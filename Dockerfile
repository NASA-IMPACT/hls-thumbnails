FROM osgeo/gdal:ubuntu-full-3.0.3

RUN apt-get update
RUN apt-get install python3-pip python3-venv -y

 
RUN pip3 install rasterio==1.1.3 --no-binary rasterio
RUN apt-get install build-essential python3-dev python3-numpy libhdf4-dev -y
RUN pip3 install tox tox-venv
RUN pip3 install --upgrade setuptools
COPY ./ ./hls_thumbnails

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["cd hls_thumbnails && tox -r"]


