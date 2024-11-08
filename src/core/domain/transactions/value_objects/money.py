from dataclasses import dataclass
from decimal import Decimal

from core.domain.transactions.entities.currency import CurrencyEntity


@dataclass(frozen=True)
class Money:
    currency: CurrencyEntity
    amount: Decimal

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.currency, self.amount + other.amount)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        return Money(self.currency, self.amount - other.amount)

    def __mul__(self, other: Decimal | int | float) -> "Money":
        if not isinstance(other, (Decimal, int, float)):
            raise ValueError("Can only multiply by a Decimal, int or float")
        return Money(self.currency, self.amount * Decimal(other))

    def __truediv__(self, other: Decimal | int | float) -> "Money":
        if not isinstance(other, (Decimal, int, float)):
            raise ValueError("Can only divide by a Decimal, int or float")
        if other == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Money(self.currency, self.amount / Decimal(other))