all: lint build test

build:
	cp app.py .gitchangelog.rc
	docker build -t release-action:latest .

lint:
	yamllint -s .
	flake8 .
	docker run --rm -i hadolint/hadolint < Dockerfile

test:
	pytest -v
