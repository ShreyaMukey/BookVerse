# Phase 2/3 Prerequisite Readiness

## Completed
- Canonical project scaffold committed on `stable/phase1-scaffold`
- FastAPI app verified locally, `/api/healthz` responds
- Local service prerequisites documented and started: PostgreSQL 14, Redis, Ollama
- Dependencies installed in `apps/api/.venv`; pytest and ruff verified green
- Setup docs created: `README.md`, `docs/SETUP.md`, `docs/PHASE2_PLAN.md`

## Prerequisites present for Phase 2
- `.env.example` at repo root
- Local Postgres database and user created
- Redis running
- Ollama service running; `gemma3:4b` downloading/pull pending completion
- Python venv and dev dependencies installed
- GitHub repo published at https://github.com/ShreyaMukey/BookVerse
- Last verified commit: `58d3d2005c519049dd02402999e129962c784a16`

## Prerequisites present for Phase 3
- Production-ready local stack documented in `docs/SETUP.md`
- Environment configuration template covers DB, Redis, OpenSearch, S3, JWT, and worker settings
- Architectural baseline documented in `docs/PHASE2_PLAN.md`

## Manual/pre-start verification commands
```bash
cd /Users/apple/Projects/BookVerse/apps/api
source .venv/bin/activate
ruff check src tests
ruff format --check src tests
python3 -m pytest tests/ -q
uvicorn bookverse.main:create_app --host 127.0.0.1 --port 8000
curl -fsS http://127.0.0.1:8000/api/healthz
ollama list
```

## Next-day ready tasks
1. Confirm Ollama model pull succeeded: `ollama pull gemma3:4b` and `ollama list`
2. Initialize Alembic: `alembic init alembic` and set `env.py` to use `models.Base.metadata`
3. Add auth endpoints under `apps/api/src/bookverse/routers/auth.py`
4. Add connector interface at `apps/api/src/bookverse/connectors/`
5. Enable runtime `.env` loading with `python-dotenv` in app startup
6. Re-run + extend pytest, then update `docs/PHASE2_PLAN.md` with exact task owners/dates
