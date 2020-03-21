# hls-thumbnails

Generate thumbnails for HLS.

## Installation

Make sure you have python development libraries and hdf4 binaries installed
in your system.

You can then install this application with `pip`:

```bash
pip install .
```

This will install the `create_thumbnail` executable on the path,
which is used as follows:

```bash
create_thumbnail -i <input_file> -o <output_file>
```

**Example usage:**

```bash
thumbnail.py -i HLS.L30.T04VER.hdf -o HLS.L30.T04VER.jpeg
```

## Testing

```bash
pytest
```
