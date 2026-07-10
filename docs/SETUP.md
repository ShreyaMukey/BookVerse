# BookVerse Setup Guide

## Verified local stack

- macOS with Homebrew
- Python 3.14 venv at `apps/api/.venv`
- PostgreSQL 14 via Homebrew services
- Redis via Homebrew services
- Ollama with `gemma3:4b`
- FastAPI app on `http://127.0.0.1:8000`
- `/api/healthz` returns HTTP 200
- pytest green; ruff green

## Install commands

```bash
# System dependencies
brew install gh python@3.14 node git redis postgresql@14 ollama

# Optional service install
brew install --cask docker
brew services start redis
brew services start postgresql@14

# Database
psql postgres -c "CREATE DATABASE bookverse;"
psql postgres -c "CREATE USER bookverse WITH PASSWORD 'bookverse' SUPERUSER;"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE bookverse TO bookverse;"

# Python
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -e ".[dev]"

# Node/pnpm
npm i -g pnpm
pnpm install

# Ollama
brew services start ollama
ollama pull gemma3:4b
```

## Run API

```bash
cd apps/api
source .venv/bin/activate
uvicorn bookverse.main:create_app --host 127.0.0.1 --port 8000
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

The canonical SQLAlchemy models are implemented in `apps/api/src/bookverse/models.py`. Additional frontmatter in `models/__init__.py` is kept as a compatibility stub.
