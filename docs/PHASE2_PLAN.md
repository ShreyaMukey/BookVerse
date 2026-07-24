# Phase 2 Implementation Plan

## Goals
- Replace demo/test-only routes with production-grade subsystems
- Add migrations, ingestion workers, embeddings/search, and auth

## Milestones

1. Alembic migrations — done
   - `apps/api/alembic/` initialized, `env.py` uses async engine + `bookverse.models.Base.metadata`, DB URL computed from `bookverse.config.settings` (not duplicated in `alembic.ini`)
   - Initial migration `1b194cbf3fde_initial_schema.py` covers all current models; `alembic upgrade head` / `downgrade base` verified round-trip against local Postgres
   - Note: async SQLAlchemy requires the `greenlet` package explicitly (not pulled in automatically by `sqlalchemy>=2.0.30` alone) — now pinned in `pyproject.toml`

2. Auth & users — partially done
   - `/auth/register`, `/auth/login`, `/auth/me` implemented in `routers/auth.py` and wired into `main.py`, verified end-to-end against local Postgres
   - Access tokens only so far — refresh tokens not yet implemented
   - `UserPreferences` scoping not yet wired to any endpoint
   - Note: `passlib[bcrypt]==1.7.4`'s backend detection is broken by `bcrypt>=4.1` (raises `ValueError: password cannot be longer than 72 bytes` on first hash call) — `bcrypt` is now pinned to `>=4.0,<4.1` in `pyproject.toml`

3. Ingestion pipeline
   - `app/bookverse/connectors/` with source interfaces
   - Implement OpenLibrary + Google Books + Gutenberg
   - Background workers for fetch, normalize, merge, enrich
   - Use `ConnectorRun` to track job state

4. Enrichment & embeddings
   - Local Ollama path for text enrichment
   - Embedding storage aligned to pgvector/OpenSearch
   - `Embedding` + `EnrichmentResult` population jobs

5. Search API
   - Semantic search over embeddings
   - Filter/search endpoints backed by PostgreSQL and OpenSearch

6. Observability
   - Structured logging, metrics, health checks for DB/Redis/Ollama/OpenSearch

## Immediate next steps
1. Add connectors skeleton plus OpenLibrary client
2. Wire `UserPreferences` to authenticated endpoints; add refresh tokens
3. Decide whether `/api/recommend` (currently implemented client-side in `apps/web` calling Anthropic directly) should move behind this API instead
