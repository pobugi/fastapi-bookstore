from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    book,
)

api_router = APIRouter()

api_router.include_router(book.router, prefix="/books", tags=["books"])
