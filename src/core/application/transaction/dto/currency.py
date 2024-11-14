from pydantic import BaseModel, Field, StringConstraints
from pydantic_core import PydanticCustomError
from typing import Annotated
from uuid import UUID

from core.domain.transaction.entities.currency import CurrencyEntity
from core.shared.utils import custom_error_msg


CurrencyCode = Annotated[
    str,
    StringConstraints(pattern=r"^[A-Z]{3}$", min_length=3, max_length=3),
    custom_error_msg(
        lambda _, __: PydanticCustomError(
            "str_error",
            f"Currency code should consist of "
            "exactly 3 uppercase letters (e.g., USD, EUR).",
        )
    ),
]


class CreateCurrencyDTO(BaseModel):
    currency_code: CurrencyCode
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
