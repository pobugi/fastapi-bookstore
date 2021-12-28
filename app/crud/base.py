from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from app.db.base_class import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.exc import DatabaseError, DisconnectionError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.sql.selectable import Select
from .errors import raise_database_error, raise_integrity_error, raise_not_found

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def object_exists(self, db: AsyncSession, id: int) -> ModelType:
        query = self.get_query_one(id=id)
        object = await self.get_or_raise(db=db, query=query)
        return object

    async def get_or_raise(self, db: AsyncSession, query: Select) -> ModelType:
        result = await db.execute(query)
        result_obj = result.scalars().first()
        raise_not_found(result_obj)
        return result_obj

    def get_query_one(self, id: int) -> Select:
        return select(self.model).filter(self.model.id == id)

    def get_query_all(self) -> Select:
        return select(self.model)

    async def get_many(
        self, db: AsyncSession, query: Select, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def create(
        self, db: AsyncSession, obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if not isinstance(obj_in, dict):
            obj_in = jsonable_encoder(obj_in, by_alias=False)
        db_obj = self.model(**obj_in)  # type: ignore
        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        except IntegrityError:
            raise_integrity_error()
        except (
            DisconnectionError,
            DatabaseError,
        ):
            raise_database_error()
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj, by_alias=False)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        except IntegrityError:
            raise_integrity_error()
        except (
            DisconnectionError,
            DatabaseError,
        ):
            raise_database_error()
        return db_obj

    async def remove(self, db: AsyncSession, id: int) -> ModelType:
        query = self.get_query_one(id=id)
        obj = await self.get_or_raise(db=db, query=query)
        try:
            await db.delete(obj)
            await db.commit()
        except (IntegrityError, UnmappedInstanceError):
            raise_integrity_error()
        except (
            DisconnectionError,
            DatabaseError,
        ):
            raise_database_error()
        return obj
