from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Args:

        `model`: A SQLAlchemy model class
        `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def create(self, db: Session, *, obj_in: SchemaType) -> ModelType:
        """Create a ModelType object"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: Any) -> ModelType:
        """Get a single ModelType filtered by id"""
        return db.query(self.model).filter(self.model.id == id).one()

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Dict[str, Any]
    ) -> ModelType:
        """Update a ModelType object"""
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> None:
        """Delete a ModelType object"""
        obj = db.query(self.model).filter(self.model.id == id).one()
        db.delete(obj)
        db.commit()
