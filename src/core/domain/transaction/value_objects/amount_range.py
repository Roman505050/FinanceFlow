from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AmountRange:
    min_amount: Decimal
    max_amount: Decimal

    def __eq__(self, other):
        return (
            self.min_amount == other.min_amount
            and self.max_amount == other.max_amount
        )

    def __ne__(self, other):
        return (
            self.min_amount != other.min_amount
            or self.max_amount != other.max_amount
        )
