from uuid import uuid4

from core.application.transaction.dto.operation import (
    CreateOperationDTO,
    OperationDTO,
)
from core.domain.transaction.entities.operation import OperationEntity
from core.domain.transaction.repositories.operation import IOperationRepository


class CreateOperationUseCase:
    def __init__(self, operation_repository: IOperationRepository):
        self._operation_repository = operation_repository

    async def execute(self, request: CreateOperationDTO) -> OperationDTO:
        """Create a new operation.

        :arg request: The operation data.
        :raise OperationAlreadyExistsException: If the operation
                                                already exists.
        :return: The created operation.
        """
        entity = OperationEntity(
            operation_id=uuid4(),
            operation_name=request.operation_name,
            operation_type=request.operation_type,
        )
        entity = await self._operation_repository.save(entity)
        return OperationDTO.from_entity(entity)
