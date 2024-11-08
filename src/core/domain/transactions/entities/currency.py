from dataclasses import dataclass
from uuid import UUID


@dataclass
class CurrencyEntity:
    currency_id: UUID
    currency_name: str
    currency_code: str
    currency_symbol: str

    def __eq__(self, other):
        return self.currency_id == other.currency_id
