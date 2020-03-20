from setuptools import setup

setup(
    name="hls_thumbnails",
    version="0.1",
    packages=['hls_thumbnails'],
    install_requires=[
        'boto3',
        'numpy',
        'rasterio',
        'Pillow',
        'pyhdf'
    ],
    extras_require={
        "develop": ["flake8"],
        "test": ["pytest", "moto"]
    },
    entry_points={
        'console_scripts': [
            'run-browse-imagery=hls_thumbnails.run_browse_imagery:download_and_create',  # noqa
        ],
    },
)
