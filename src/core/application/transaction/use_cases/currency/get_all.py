from core.application.transaction.dto.currency import CurrencyDTO
from core.domain.transaction.repositories.currency import ICurrencyRepository


class GetAllCurrencyUseCase:
    def __init__(self, currency_repository: ICurrencyRepository):
        self._currency_repository = currency_repository

    async def execute(self) -> list[CurrencyDTO]:
        """Get all currencies.

        :return: The currencies.
        """
        entities = await self._currency_repository.get_all()
        return [CurrencyDTO.from_entity(entity) for entity in entities]
