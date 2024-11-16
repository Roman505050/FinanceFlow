from dataclasses import dataclass
from uuid import UUID
import re


@dataclass
class CurrencyEntity:
    currency_id: UUID
    currency_name: str
    currency_code: str  # ISO 4217 code
    currency_symbol: str

    def __post_init__(self):
        self._validate()

    def _validate(self):
        self._validate_currency_code(self.currency_code)
        if not 3 <= len(self.currency_name) <= 64:
            raise ValueError(
                "Currency name must be between 3 and 64 characters"
            )
        if not 1 <= len(self.currency_symbol) <= 8:
            raise ValueError(
                "Currency symbol must be between 1 and 8 characters"
            )

    @staticmethod
    def _validate_currency_code(code: str):
        if not len(code) == 3 and re.match("^[A-Z]{3}$", code):
            raise ValueError(
                "Currency code must be a 3-letter uppercase string"
            )

    def __eq__(self, other):
        return self.currency_id == other.currency_id

    def __ne__(self, other):
        return self.currency_id != other.currency_id
