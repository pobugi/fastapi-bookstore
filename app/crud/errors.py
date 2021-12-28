from typing import TypeVar, Union, Optional

from app.db.base_class import Base
from fastapi import HTTPException

ModelType = TypeVar("ModelType", bound=Base)


def raise_not_found(
    result_obj: Union[ModelType, None],
    model_name: str = "Object",
    message: str = "not found",
) -> None:
    if result_obj is None:
        raise HTTPException(status_code=404, detail=f"{model_name} {message}")


def raise_integrity_error(
    model_name: str = "Object", message: str = "cannot be processed"
) -> Optional[HTTPException]:
    raise HTTPException(status_code=422, detail=f"{model_name} {message}")


def raise_database_error(message: str = "Database error") -> Optional[HTTPException]:
    raise HTTPException(status_code=500, detail=message)
