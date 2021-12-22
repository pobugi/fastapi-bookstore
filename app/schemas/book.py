from pydantic import BaseModel, Field
from pydantic.types import PositiveInt


class CustomBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class BookBase(CustomBaseModel):
    title: str = Field("Book title", min_length=2, max_length=50)
    author: str = Field("Book title", min_length=2, max_length=50)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookInDBBase(BookBase):
    pass


class Book(BookInDBBase):
    pass


class BookInDB(BookInDBBase):
    pass
