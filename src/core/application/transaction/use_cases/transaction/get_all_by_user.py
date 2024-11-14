from uuid import UUID

from core.application.transaction.dto.transaction import TransactionDTO
from core.domain.transaction.filters.transaction import TransactionFilters
from core.domain.transaction.repositories.transaction import (
    ITransactionRepository,
)


class GetAllTransactionsByUserUseCase:
    def __init__(self, transaction_repository: ITransactionRepository):
        self._transaction_repository = transaction_repository

    async def execute(self, user_id: UUID) -> list[TransactionDTO]:
        """Get all transactions by user id.

        :arg user_id: The user id.
        :return: The transactions.
        """
        filters = TransactionFilters(user_id=user_id)
        transactions = await self._transaction_repository.get_by_filters(
            filters
        )
        return [
            TransactionDTO.from_entity(transaction)
            for transaction in transactions
        ]
