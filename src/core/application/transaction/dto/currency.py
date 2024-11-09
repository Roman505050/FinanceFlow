from pydantic import BaseModel, Field
from uuid import UUID

from core.domain.transaction.entities.currency import CurrencyEntity


class CreateCurrencyDTO(BaseModel):
    currency_code: str = Field(
        min_length=3, max_length=3, pattern="^[A-Z]{3}$"
    )
    currency_name: str = Field(min_length=3, max_length=64)
    currency_symbol: str = Field(min_length=1, max_length=8)


class CurrencyDTO(CreateCurrencyDTO):
    currency_id: UUID

    @staticmethod
    def from_entity(entity: CurrencyEntity) -> "CurrencyDTO":
        return CurrencyDTO(
            currency_id=entity.currency_id,
            currency_code=entity.currency_code,
            currency_name=entity.currency_name,
            currency_symbol=entity.currency_symbol,
        )
