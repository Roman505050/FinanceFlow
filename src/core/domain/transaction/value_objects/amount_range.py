from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AmountRange:
    min_amount: Decimal
    max_amount: Decimal
