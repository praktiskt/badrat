.PHONY: generate dev-fastapi dev-baml docker-build docker-tag docker-push

IMAGE_NAME ?= badrat
IMAGE_TAG ?= build

generate:
	uv run baml-cli generate --from=src

dev-fastapi:
	cd src && uv run fastapi dev

dev-baml:
	uv run baml-cli dev --from=src --preview

docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-tag: docker-build
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) praktiskt/$(IMAGE_NAME):latest

docker-push: docker-tag
	docker push praktiskt/$(IMAGE_NAME):latest
