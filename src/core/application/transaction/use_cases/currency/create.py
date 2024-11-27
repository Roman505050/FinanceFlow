from uuid import uuid4

from core.application.transaction.dto.currency import (
    CreateCurrencyDTO,
    CurrencyDTO,
)
from core.domain.transaction.entities.currency import CurrencyEntity
from core.domain.transaction.repositories.currency import ICurrencyRepository


class CreateCurrencyUseCase:
    def __init__(self, currency_repository: ICurrencyRepository):
        self._currency_repository = currency_repository

    async def execute(self, request: CreateCurrencyDTO) -> CurrencyDTO:
        """Create a new currency.

        :arg request: The currency data.
        :raise CurrencyAlreadyExistException: If the currency
                                               already exists.
        :return: The created currency.
        """
        entity = CurrencyEntity(
            currency_id=uuid4(),
            currency_name=request.currency_name,
            currency_symbol=request.currency_symbol,
            currency_code=request.currency_code,
        )
        entity = await self._currency_repository.save(entity)
        return CurrencyDTO.from_entity(entity)
