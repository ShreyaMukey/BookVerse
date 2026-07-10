from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from bookverse.db import get_session_factory

router = APIRouter(prefix="/authors", tags=["authors"])
session_factory = get_session_factory()


@router.get("")
async def list_authors(limit: int = 20, offset: int = 0):
    from bookverse.models import CanonicalAuthor

    async with session_factory() as session:
        stmt = select(CanonicalAuthor).order_by(CanonicalAuthor.updated_at.desc()).limit(limit).offset(offset)
        result = await session.execute(stmt)
        authors = result.scalars().all()
    return {"count": len(authors), "results": [{"id": str(a.id), "name": a.name} for a in authors]}


@router.get("/{author_id}")
async def get_author(author_id: str):
    from bookverse.models import CanonicalAuthor

    async with session_factory() as session:
        author = await session.get(CanonicalAuthor, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="author_not_found")
        return {"id": str(author.id), "name": author.name}
