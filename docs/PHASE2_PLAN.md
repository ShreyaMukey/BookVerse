# Phase 2 Implementation Plan

## Goals
- Replace demo/test-only routes with production-grade subsystems
- Add migrations, ingestion workers, embeddings/search, and auth

## Milestones

1. Alembic migrations
   - Add `alembic` to `apps/api/pyproject.toml`
   - Create `apps/api/alembic/` with initial migration for `models.py`
   - Add `alembic upgrade head` to local runbook

2. Auth & users
   - `/auth/register`, `/auth/login`, `/auth/me`
   - JWT + refresh tokens
   - `UserProfile` + `UserPreferences` scoped to logged-in users

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
1. Add Alembic init + first migration for `models.py`
2. Add `/auth` routers
3. Add connectors skeleton plus OpenLibrary client
