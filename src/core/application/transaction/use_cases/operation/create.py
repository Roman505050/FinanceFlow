from core.application.transaction.dto.operation import (
    CreateOperationDTO,
    OperationDTO,
)
from core.application.transaction.factories.operation import OperationFactory
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
        entity = OperationFactory.create(operation_name=request.operation_name)
        entity = await self._operation_repository.save(entity)
        await self._operation_repository.commit()
        return OperationDTO.from_entity(entity)
