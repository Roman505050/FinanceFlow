from pydantic import BaseModel, Field
from uuid import UUID

from core.domain.transaction.entities.operation import OperationEntity


class CreateOperationDTO(BaseModel):
    operation_name: str = Field(min_length=3, max_length=64)


class OperationDTO(CreateOperationDTO):
    operation_id: UUID

    @staticmethod
    def from_entity(entity: OperationEntity) -> "OperationDTO":
        return OperationDTO(
            operation_id=entity.operation_id,
            operation_name=entity.operation_name,
        )
