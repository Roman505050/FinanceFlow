from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID

from core.domain.transaction.entities.operation import OperationEntity
from core.domain.transaction.enums.operation import (
    get_operation_type_string,
)


class CreateOperationDTO(BaseModel):
    operation_name: str = Field(min_length=3, max_length=64)
    operation_type: Literal["income", "expense", "investment"]


class OperationDTO(CreateOperationDTO):
    operation_id: UUID

    @staticmethod
    def from_entity(entity: OperationEntity) -> "OperationDTO":
        return OperationDTO(
            operation_id=entity.operation_id,
            operation_name=entity.operation_name,
            operation_type=get_operation_type_string(entity.operation_type),
        )
