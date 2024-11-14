from uuid import UUID

from core.domain.transaction.repositories.operation import IOperationRepository


class DeleteOperationUseCase:
    def __init__(self, operation_repository: IOperationRepository):
        self._operation_repository = operation_repository

    async def execute(self, operation_id: UUID) -> None:
        """
        Delete an operation.

        :arg operation_id: The operation id.
        :raise OperationNotFoundException: If the operation does not exist.
        :raise OperationNotDeletableException: If the operation
                                                is not deletable.
        :return: None
        """
        await self._operation_repository.delete(operation_id)
