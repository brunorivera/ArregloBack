"""
Module for Base Service Implementation
"""
from typing import List, Type
from sqlalchemy.orm import Session
from models.base_model import BaseModel
from services.base_service import BaseService
from repositories.base_repository import BaseRepository
from schemas.base_schema import BaseSchema


class BaseServiceImpl(BaseService):
    """Base Service Implementation"""

    def __init__(self, repository_class: Type[BaseRepository],
                 model: Type[BaseModel],
                 schema: Type[BaseSchema],
                 db: Session):
        self._repository_class = repository_class
        self._repository = repository_class(db)
        self._model = model
        self._schema = schema

    @property
    def repository(self) -> BaseRepository:
        """Repository to access database"""
        return self._repository

    @property
    def schema(self) -> BaseSchema:
        """Pydantic Schema to validate data"""
        return self._schema

    @property
    def model(self) -> BaseModel:
        """SQLAlchemy Model"""
        return self._model

    def get_all(self, skip: int = 0, limit: int = 100) -> List[BaseSchema]:
        """Get all data with pagination"""
        return self.repository.find_all(skip=skip, limit=limit)

    def get_one(self, id_key: int) -> BaseSchema:
        """Get one data"""
        return self.repository.find(id_key)

    def save(self, schema: BaseSchema) -> BaseSchema:
        """Save data"""
        return self.repository.save(self.to_model(schema))

    def update(self, id_key: int, schema: BaseSchema) -> BaseSchema:
        """Update data"""
        return self.repository.update(id_key, schema.model_dump(exclude_unset=True))

    def delete(self, id_key: int) -> None:
        """Delete data"""
        self.repository.remove(id_key)

    def to_model(self, schema: BaseSchema) -> BaseModel:
        """
        Convert schema to a SQLAlchemy model instance, excluding relationship fields.
        This method intelligently extracts only the columns that belong to the
        target model, ignoring any nested relationship data present in the schema.
        This prevents `AttributeError` during model instantiation when schemas
        contain nested objects.
        """
        from sqlalchemy import inspect
        model_class = self.model
        schema_data = schema.model_dump(exclude_unset=True)
        relationship_keys = {rel.key for rel in inspect(model_class).relationships}
        model_data = {
            key: value for key, value in schema_data.items()
            if key not in relationship_keys
        }
        return model_class(**model_data)
