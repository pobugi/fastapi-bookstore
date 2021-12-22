from app.crud.base import CRUDBase
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from sqlalchemy.sql.selectable import Select


class CRUDItem(CRUDBase[Book, BookCreate, BookUpdate]):
    pass


book = CRUDItem(Book)
