from core.application.transaction.dto.transaction import (
    CreateTransactionDTO,
    TransactionDTO,
)
from core.application.transaction.factories.transaction import (
    TransactionFactory,
)
from core.domain.transaction.repositories.transaction import (
    ITransactionRepository,
)
from core.domain.transaction.repositories.category import ICategoryRepository
from core.domain.transaction.repositories.currency import ICurrencyRepository


class CreateTransactionUseCase:
    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        category_repository: ICategoryRepository,
        currency_repository: ICurrencyRepository,
    ):
        self._transaction_repository = transaction_repository
        self._category_repository = category_repository
        self._currency_repository = currency_repository

    async def execute(self, request: CreateTransactionDTO) -> TransactionDTO:
        """Create a new transaction.

        :arg request: The transaction data.
        :raise CategoryNotFoundException: If the operation does not exist.
        :raise CurrencyNotFoundException: If the currency does not exist.
        :return: The created transaction.
        """
        category = await self._category_repository.get_by_id(
            category_id=request.category_id
        )

        currency = await self._currency_repository.get_by_id(
            currency_id=request.currency_id
        )

        entity = TransactionFactory.create(
            user_id=request.user_id,
            category=category,
            currency=currency,
            amount=request.amount,
            date=request.date,
            description=request.description,
        )
        entity = await self._transaction_repository.save(entity)
        await self._transaction_repository.commit()
        return TransactionDTO.from_entity(entity)