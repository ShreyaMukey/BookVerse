# BookVerse Architecture

## Canonical schema
- One canonical schema. No provider models leak into app code.
- All records store `source`, `source_id`, `source_updated_at`, `confidence`, `version`.
- Dedupe by ISBN-13, ISBN-10, OpenLibrary work ID, Google Books ID, then author/title/year.

## Connectors
- Each provider is an adapter implementing incremental sync, full sync, retries, rate limiting, dedupe, logging, versioning, validation, and change detection.
- Connectors only write canonical records through the merge engine.

## Ingestion
- Celery workers run connectors on schedules.
- Connector runs are tracked in `connector_run`.
- Merge outcomes are logged in `merge_log`.

## Search
- OpenSearch for full-text, synonyms, typo tolerance, faceting.
- pgvector for semantic similarity.

## Recommendations
- Hybrid: content-based, collaborative, vector similarity, popularity, novelty, diversity.
- Configurable weights by feed.

## Frontend
- Next.js 14 app router.
- Three independent ranked feeds on homepage: best overall, popular, hidden gems.
