# BookVerse

BookVerse is a knowledge discovery platform for books. Phase 1 delivers a production-style local-on-prem scaffold with FastAPI, canonical PostgreSQL schema, background ingestion workers, search-ready indexing, and an offline-capable local LLM path.

## Verified local stack

- FastAPI app starts and `/api/healthz` returns HTTP 200 `{"status":"ok","service":"bookverse-api"}`
- PostgreSQL 14 running locally with `bookverse` database
- Redis running locally
- Ollama running locally
- Python venv installed with dev deps; pytest green; ruff green

## Quick start

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -e ".[dev]"

export DATABASE_URL=postgresql+asyncpg://bookverse:bookverse@127.0.0.1:5432/bookverse
export REDIS_URL=redis://127.0.0.1:6379/0

uvicorn bookverse.main:create_app --reload
```

## Docs

See `docs/SETUP.md` and `docs/ARCHITECTURE.md`.

## LLM providers

See `docs/LLM_PROVIDERS.md`.

## Phase 2 focus

Ingestion connectors, Alembic migrations, OpenSearch indexing, and auth hardening.
