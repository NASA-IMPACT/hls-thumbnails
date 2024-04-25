import os.path
from setuptools import setup

with open(os.path.join("hls_thumbnails", "VERSION")) as version_file:
    version = version_file.read().strip()

setup(
    name="hls_thumbnails",
    version=version,
    packages=["hls_thumbnails"],
    include_package_data=True,
    install_requires=[
        "numpy",
        "rasterio",
        "Pillow",
        "pyhdf==0.10.5",
    ],
    extras_require={"test": ["flake8", "pytest"]},
    entry_points={
        "console_scripts": [
            "create_thumbnail=hls_thumbnails.create_thumbnail:create_thumbnail"
        ],
    },
)
