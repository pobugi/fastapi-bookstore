from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from app.db.base_class import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.exc import DatabaseError, DisconnectionError, IntegrityError
from sqlalchemy.orm import Query, Session

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

    def get_or_raise(self, db: Session, id: Any) -> ModelType:
        result = db.query(self.model).filter(self.model.id == id).first()
        # raise_not_found(result)
        return result

    def get_query(self, db: Session) -> Query:
        return db.query(self.model)

    def get_many(
        self, query: Query, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return query.offset(skip).limit(limit).all()

    def get_one_or_raise(self, query: Query) -> ModelType:
        result = query.first()
        # raise_not_found(result)
        return result

    def create(
        self, db: Session, obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if not isinstance(obj_in, dict):
            obj_in = jsonable_encoder(obj_in, by_alias=False)
        db_obj = self.model(**obj_in)  # type: ignore
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            pass
            # raise_integrity_error()
        except (
            DisconnectionError,
            DatabaseError,
        ):
            pass
            # raise_database_error()
        return db_obj

    def update(
        self,
        db: Session,
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
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            pass
            # raise_integrity_error()
        except (
            DisconnectionError,
            DatabaseError,
        ):
            pass
            # raise_database_error()
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        try:
            db.delete(obj)
            db.commit()
        except IntegrityError:
            pass
            # raise_integrity_error()
        except (
            DisconnectionError,
            DatabaseError,
        ):
            pass
            # raise_database_error()
        return obj
