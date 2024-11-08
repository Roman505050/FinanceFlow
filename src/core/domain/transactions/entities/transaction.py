from dataclasses import dataclass
from uuid import UUID
import datetime

from core.domain.transactions.entities.category import CategoryEntity
from core.domain.transactions.value_objects.money import Money


@dataclass
class TransactionEntity:
    transactions_id: UUID
    user_id: UUID
    category: CategoryEntity
    money: Money
    description: str
    data: datetime.datetime


