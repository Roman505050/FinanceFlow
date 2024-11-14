from uuid import UUID

from core.domain.transaction.repositories.currency import ICurrencyRepository


class DeleteCurrencyUseCase:
    def __init__(self, currency_repository: ICurrencyRepository):
        self._currency_repository = currency_repository

    async def execute(self, currency_id: UUID) -> None:
        """
        Delete a currency.

        :param currency_id: The currency id.
        :raise CurrencyNotFoundException: If the currency does not exist.
        :raise CurrencyNotDeletableException: If the currency is not deletable.
        :return:
        """
        await self._currency_repository.delete(currency_id)
