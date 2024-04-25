VERSION = $$(<hls_thumbnails/VERSION)
DOCKER_IMAGE ?= "hls-thumbnails:$(VERSION)"

.PHONY: docker-build docker-run

docker-build:
	docker build -t $(DOCKER_IMAGE) .

docker-run: docker-build
	docker run -it --rm $(DOCKER_IMAGE)
