.PHONY: help install api web worker test lint fmt migrate shell compose-up compose-down clean

help:
	@echo "BookVerse dev targets"

install:
	cd apps/api && python3 -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]"
	cd apps/web && npm install

api:
	cd apps/api && source .venv/bin/activate && uvicorn bookverse.main:create_app --factory --reload --port 8000

web:
	cd apps/web && npm run dev

worker:
	cd worker && celery -A bookverse.tasks worker -Q ingestion -c 4 -l info

test:
	pytest apps/api/tests -q

lint:
	ruff check apps/api/src bookverse tests

fmt:
	ruff format apps/api/src tests

migrate:
	cd apps/api && alembic upgrade head

compose-up:
	docker compose -f infra/compose/docker-compose.yml up -d

compose-down:
	docker compose -f infra/compose/docker-compose.yml down

shell:
	@echo "Local connect shell placeholder."

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + || true
