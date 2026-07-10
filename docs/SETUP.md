# BookVerse SETUP

## Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 16 with `uuid-ossp` and `pgvector` extensions
- Redis 7
- OpenSearch 2.x
- MinIO

## Quick start
```bash
cp infra/compose/.env.example infra/compose/.env
docker compose -f infra/compose/docker-compose.yml up -d
cd apps/api && python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
uvicorn bookverse.main:create_app --factory --reload --port 8000
```

## Tests
```bash
pytest apps/api/tests -q
```

## Web app
```bash
cd apps/web
npm install
npm run dev
```
