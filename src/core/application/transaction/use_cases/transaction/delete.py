from uuid import UUID

from core.domain.transaction.repositories.transaction import (
    ITransactionRepository,
)


class DeleteTransactionUseCase:
    def __init__(self, transaction_repository: ITransactionRepository) -> None:
        self._transaction_repository = transaction_repository

    async def execute(self, transaction_id: UUID) -> None:
        """
        Delete a transaction.

        :param transaction_id: The transaction id.
        :raise TransactionNotFoundException: If the transaction does not exist.
        :return: None
        """
        await self._transaction_repository.delete(transaction_id)
        await self._transaction_repository.commit()
