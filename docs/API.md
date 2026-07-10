# BookVerse API

Base path is set by `API_PREFIX`, default `/api`.

## Endpoints
- `GET /api/healthz`
- `GET /api/books`
- `GET /api/books/{id}`
- `GET /api/authors`
- `GET /api/authors/{id}`
- `GET /api/search/books`

## Feed shape (phase 1)
- `GET /api/feeds/overall`
- `GET /api/feeds/popular`
- `GET /api/feeds/hidden-gems`
