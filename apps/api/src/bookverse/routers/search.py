from fastapi import APIRouter

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/books")
async def search_books(q: str = ""):
    if not q:
        return {"count": 0, "results": []}
    return {"count": 0, "results": [], "note": "OpenSearch integration in Phase 2."}
