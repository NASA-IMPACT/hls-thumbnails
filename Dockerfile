# Test if this module can be installed on top of the HLS-Sentinel image.

FROM 018923174646.dkr.ecr.us-west-2.amazonaws.com/hls-sentinel:latest
RUN pip install --upgrade awscli numpy && pip install --ignore-installed pyparsing


COPY . ${SRC_DIR}/hls-thumbnails
WORKDIR ${SRC_DIR}/hls-thumbnails

RUN pip install -e .['test']

ENTRYPOINT ["/bin/sh", "-c"]

# Also run the actual tests.
CMD ["pytest"]
