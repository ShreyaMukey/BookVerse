from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from bookverse.db import async_session_factory
from bookverse.models import CanonicalBook, BookCategory, SourceType

router = APIRouter(prefix="/books", tags=["books"])


@router.get("")
async def list_books(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    async with async_session_factory() as session:
        stmt = (
            select(CanonicalBook)
            .order_by(CanonicalBook.popularity_score.desc().nullslast(), CanonicalBook.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(stmt)
        books = result.scalars().all()
    return {"count": len(books), "results": [{"id": str(b.id), "title": b.title} for b in books]}


@router.get("/{book_id}")
async def get_book(book_id: str):
    async with async_session_factory() as session:
        book = await session.get(CanonicalBook, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="book_not_found")
        return {"id": str(book.id), "title": book.title, "publication_year": book.publication_year}
