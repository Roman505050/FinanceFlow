from uuid import UUID

from core.domain.transaction.repositories.transaction import (
    ITransactionRepository,
)
from core.shared.exceptions import ForbiddenException


class DeleteTransactionUseCase:
    def __init__(self, transaction_repository: ITransactionRepository) -> None:
        self._transaction_repository = transaction_repository

    async def execute(self, user_id: UUID, transaction_id: UUID) -> None:
        """
        Delete a transaction.

        :param user_id: The user id that is trying to delete the transaction.
        :param transaction_id: The transaction id.
        :raise ForbiddenException: If the user is not allowed to
                                    delete the transaction.
        :raise TransactionNotFoundException: If the transaction does not exist.
        :return: None
        """
        transaction = await self._transaction_repository.get_by_id(
            transaction_id
        )

        if transaction.user_id != user_id:
            raise ForbiddenException(
                "You are not allowed to delete this transaction"
            )

        await self._transaction_repository.delete(transaction_id)
