from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bookverse.config import settings
from bookverse.routers.auth import router as auth_router
from bookverse.routers.authors import router as authors_router
from bookverse.routers.books import router as books_router
from bookverse.routers.health import router as health_router
from bookverse.routers.search import router as search_router


def create_app() -> FastAPI:
    the_app = FastAPI(
        title="BookVerse API",
        description="Universal Book Intelligence Platform",
        version=settings.app_version,
        root_path=settings.api_prefix,
    )

    the_app.add_middleware(
        CORSMiddleware,
        allow_origins=[c.strip() for c in settings.cors_origins.split(",") if c.strip()],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    the_app.include_router(health_router)
    the_app.include_router(books_router)
    the_app.include_router(authors_router)
    the_app.include_router(search_router)
    the_app.include_router(auth_router)

    return the_app
