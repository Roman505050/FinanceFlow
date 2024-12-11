from core.application.transaction.dto.operation import OperationDTO
from core.domain.transaction.repositories.operation import IOperationRepository


class GetAllOperationUseCase:
    def __init__(self, operation_repository: IOperationRepository):
        self._operation_repository = operation_repository

    async def execute(self) -> list[OperationDTO]:
        """Get all operations.

        :return: The operations.
        """
        entities = await self._operation_repository.get_all()
        return [OperationDTO.from_entity(entity) for entity in entities]
