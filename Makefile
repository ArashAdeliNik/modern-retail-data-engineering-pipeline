.PHONY: local test lint generate ingest up down logs

local:
	python -m src.pipeline all --rows 500

test:
	pytest -q

lint:
	ruff check src tests dashboard

generate:
	python -m src.pipeline generate --rows 500

ingest:
	python -m src.pipeline ingest

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

