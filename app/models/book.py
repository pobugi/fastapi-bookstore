from app.db.base_class import Base
from sqlalchemy import Column, Integer, String


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)

    def __str__(self) -> str:
        return f"Book: {self.title} by {self.author}"
