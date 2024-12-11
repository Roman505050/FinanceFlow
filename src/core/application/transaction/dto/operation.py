from uuid import UUID

from pydantic import BaseModel, Field

from core.domain.transaction.entities.operation import OperationEntity
from core.domain.transaction.enums.operation import OperationType


class CreateOperationDTO(BaseModel):
    operation_name: str = Field(min_length=3, max_length=64)
    operation_type: OperationType


class OperationDTO(CreateOperationDTO):
    operation_id: UUID

    @staticmethod
    def from_entity(entity: OperationEntity) -> "OperationDTO":
        return OperationDTO(
            operation_id=entity.operation_id,
            operation_name=entity.operation_name,
            operation_type=entity.operation_type,
        )
