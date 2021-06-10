all: lint build test

build:
	docker build -t release-action:latest .

lint:
	yamllint -s .
	flake8 .
	docker run --rm -i hadolint/hadolint < Dockerfile

test:
	pytest -v
