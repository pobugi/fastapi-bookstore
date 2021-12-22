from typing import List

from app import crud, schemas
from app.api import deps
from app.models.book import Book
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.book import BookCreate

router = APIRouter()


@router.get("/", response_model=List[schemas.Book])
def get_all_books(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[Book]:
    query = crud.book.get_query(db=db)
    result = crud.book.get_many(query=query, skip=skip, limit=limit)
    return result


@router.get("/{id}", response_model=schemas.Book)
def get_book(
    id: int,
    db: Session = Depends(deps.get_db),
) -> Book:
    result = crud.book.get_or_raise(db=db, id=id)
    return result


@router.post("/", response_model=schemas.Book)
def create_book(
    book_in: schemas.BookCreate,
    db: Session = Depends(deps.get_db),
) -> Book:
    result = crud.book.create(db=db, obj_in=book_in)
    return result


@router.put("/{id}", response_model=schemas.Book)
def update_book(
    id: int,
    book_in: schemas.BookUpdate,
    db: Session = Depends(deps.get_db),
) -> Book:
    book_obj = crud.book.get_or_raise(db=db, id=id)
    book_obj = crud.book.update(db=db, db_obj=book_obj, obj_in=book_in)
    return book_obj


@router.delete("/{id}", response_model=schemas.Book)
def delete_book(
    id: int,
    db: Session = Depends(deps.get_db),
) -> Book:
    book_obj = crud.book.get_or_raise(db=db, id=id)
    book_obj = crud.book.remove(db=db, id=id)
    return book_obj
