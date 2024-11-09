from uuid import uuid4

from core.domain.transaction.entities.currency import CurrencyEntity


class CurrencyFactory:
    @staticmethod
    def create(
        currency_name: str, currency_code: str, currency_symbol: str
    ) -> CurrencyEntity:
        return CurrencyEntity(
            currency_id=uuid4(),
            currency_name=currency_name,
            currency_code=currency_code,
            currency_symbol=currency_symbol,
        )
