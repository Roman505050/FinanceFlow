from dataclasses import dataclass
from uuid import UUID
import datetime

from core.domain.transaction.entities.category import CategoryEntity
from core.domain.transaction.value_objects.money import Money


@dataclass
class TransactionEntity:
    transactions_id: UUID
    user_id: UUID
    category: CategoryEntity
    money: Money
    description: str
    data: datetime.datetime

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not 10 <= len(self.description) <= 255:
            raise ValueError(
                "Description must be between 10 and 64 characters"
            )
