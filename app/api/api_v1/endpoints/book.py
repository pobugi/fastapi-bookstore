from typing import List

from app import crud, schemas
from app.api import deps
from app.models.book import Book
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=List[schemas.Book])
async def get_all_books(
    db: AsyncSession = Depends(deps.get_db_async),
    skip: int = 0,
    limit: int = 100,
) -> List[Book]:
    query = crud.book.get_query_all()
    result = await crud.book.get_many(db=db, query=query, skip=skip, limit=limit)
    return result


@router.post("/", status_code=201, response_model=schemas.BookCreate)
async def add_book(
    book_in: schemas.BookCreate,
    db: AsyncSession = Depends(deps.get_db_async),
) -> Book:
    result = await crud.book.create(db=db, obj_in=book_in)
    return result


@router.put("/{id}", response_model=schemas.BookUpdate)
async def update_book(
    id: int,
    book_in: schemas.BookUpdate,
    db: AsyncSession = Depends(deps.get_db_async),
) -> Book:
    query = crud.book.get_query_one(id=id)
    book_obj = await crud.book.get_or_raise(db=db, query=query)
    result = await crud.book.update(db=db, db_obj=book_obj, obj_in=book_in)
    return result


@router.get("/{id}", response_model=schemas.Book)
async def get_book(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
) -> Book:
    query = crud.book.get_query_one(id=id)
    result = await crud.book.get_or_raise(db=db, query=query)
    return result


@router.delete("/{id}", response_model=schemas.Book)
async def delete_book(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
) -> Book:
    return await crud.book.remove(db=db, id=id)
