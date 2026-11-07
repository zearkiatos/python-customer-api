.PHONY: activate

activate:
	@if [ ! -d venv ]; then \
		python3 -m venv venv; \
		echo "The environment folder was created and the python 🐍 environment was activated"; \
	else \
		echo "Python 🐍 environment was activated"; \
	fi

install:
	pip3 install -r requirements.txt

run:
	fastapi dev src/main.py

docker-local-up:
	docker-compose -f docker-compose.local.yaml up -d --build

docker-local-down:
	docker-compose -f docker-compose.local.yaml down

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

podman-local-up:
	podman-compose -f docker-compose.local.yaml up -d --build

podman-local-down:
	podman-compose -f docker-compose.local.yaml down

podman-up:
	podman-compose up -d --build

podman-down:
	podman-compose down