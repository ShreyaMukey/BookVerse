from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bookverse.db import async_session_factory
from bookverse.models import CanonicalAuthor

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("")
async def list_authors(limit: int = 20, offset: int = 0):
    async with async_session_factory() as session:
        stmt = select(CanonicalAuthor).order_by(CanonicalAuthor.updated_at.desc()).limit(limit).offset(offset)
        result = await session.execute(stmt)
        authors = result.scalars().all()
    return {"count": len(authors), "results": [{"id": str(a.id), "name": a.name} for a in authors]}


@router.get("/{author_id}")
async def get_author(author_id: str):
    async with async_session_factory() as session:
        author = await session.get(CanonicalAuthor, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="author_not_found")
        return {"id": str(author.id), "name": author.name}
