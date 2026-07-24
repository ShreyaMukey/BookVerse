# BookVerse Setup Guide

## Verified local stack

- macOS with Homebrew
- Python 3.11 venv at `apps/api/.venv` (system `python3` may be older — install via `brew install python@3.11` or similar and point the venv at that interpreter)
- PostgreSQL 16 via Homebrew services (matches `infra/compose/docker-compose.yml`'s `pgvector/pgvector:pg16` image)
- Redis via Homebrew services
- Ollama with `gemma3:4b`
- FastAPI app on `http://127.0.0.1:8000`
- `/api/healthz` returns HTTP 200
- pytest green; ruff green
- Alembic migrations apply cleanly (`alembic upgrade head` / `alembic downgrade base`)
- `/auth/register`, `/auth/login`, `/auth/me` verified end-to-end against a local Postgres

## Install commands

```bash
# System dependencies
brew install gh python@3.11 node git redis postgresql@16 ollama

# Optional service install
brew install --cask docker
brew services start redis
brew services start postgresql@16

# Database
psql postgres -c "CREATE DATABASE bookverse;"
psql postgres -c "CREATE USER bookverse WITH PASSWORD 'bookverse' SUPERUSER;"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE bookverse TO bookverse;"

# Python (must be 3.11+; check with python3 -V first)
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -e ".[dev]"

# Frontend
cd ../web
npm install

# Ollama
brew services start ollama
ollama pull gemma3:4b
```

## Run API

```bash
cd apps/api
source .venv/bin/activate
alembic upgrade head
uvicorn bookverse.main:create_app --host 127.0.0.1 --port 8000
```

## Run web

```bash
cd apps/web
cp .env.local.example .env.local   # then fill in ANTHROPIC_API_KEY
npm run dev
```

## Database migrations

```bash
cd apps/api
source .venv/bin/activate
alembic upgrade head                              # apply all migrations
alembic revision --autogenerate -m "description"  # generate a new migration after changing models.py
alembic downgrade -1                              # roll back one migration
```

## Health check

```bash
curl -fsS http://127.0.0.1:8000/api/healthz
# {"status":"ok","service":"bookverse-api"}
```

## Tests and lint

```bash
cd apps/api
source .venv/bin/activate
ruff check src tests
ruff format --check src tests
python3 -m pytest tests/ -q
```

## Env

Use `apps/api/.env` locally. See `infra/compose/.env.example` for service values.

## Phase 1 note

The canonical SQLAlchemy models are implemented in `apps/api/src/bookverse/models.py` — there is no separate `models/` package.
