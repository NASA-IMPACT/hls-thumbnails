from setuptools import setup

setup(
    name="hls_thumbnails",
    version="0.1",
    packages=["hls_thumbnails"],
    install_requires=["numpy", "rasterio", "Pillow", "pyhdf"],
    extras_require={"test": ["flake8", "pytest"]},
    entry_points={
        "console_scripts": [
            "create_thumbnail=hls_thumbnails.create_thumbnail:create_thumbnail"
        ],
    },
)
