from pydantic import BaseModel, Field
from uuid import UUID

from core.domain.transaction.entities.category import CategoryEntity


class CreateCategoryDTO(BaseModel):
    category_name: str = Field(min_length=3, max_length=64)
    operation_id: UUID


class CategoryDTO(BaseModel):
    category_id: UUID
    category_name: str
    operation_name: str

    @staticmethod
    def from_entity(entity: CategoryEntity) -> "CategoryDTO":
        return CategoryDTO(
            category_id=entity.category_id,
            category_name=entity.category_name,
            operation_name=entity.operation.operation_name,
        )
