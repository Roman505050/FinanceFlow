from decimal import Decimal
from uuid import uuid4, UUID
import datetime

from core.domain.transaction.entities.category import CategoryEntity
from core.domain.transaction.entities.currency import CurrencyEntity
from core.domain.transaction.entities.transaction import TransactionEntity
from core.domain.transaction.value_objects.money import Money


class TransactionFactory:
    @staticmethod
    def create(
        user_id: UUID,
        category: CategoryEntity,
        currency: CurrencyEntity,
        amount: Decimal,
        description: str | None,
        date: datetime.datetime,
    ) -> TransactionEntity:
        return TransactionEntity(
            transaction_id=uuid4(),
            user_id=user_id,
            category=category,
            money=Money(
                currency=currency,
                amount=amount,
            ),
            description=description,
            date=date,
        )
