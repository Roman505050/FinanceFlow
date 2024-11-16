from sqlalchemy import String, ForeignKey, DECIMAL, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
)
from decimal import Decimal
from uuid import uuid4, UUID
import datetime

from core.domain.transaction.value_objects.money import Money
from core.domain.transaction.entities.transaction import TransactionEntity
from core.infrastructure.database.models.base import (
    Base,
    updated_at,
)
from core.infrastructure.database.models.category import Category
from core.infrastructure.database.models.currency import Currency


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey(
            "users.user_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    category_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey(
            "categories.category_id",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    currency_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey(
            "currencies.currency_id",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=10, scale=2),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    updated_at: Mapped[updated_at]

    category: Mapped[Category] = relationship(
        "Category",
        backref="categories",
    )
    currency: Mapped[Currency] = relationship(
        "Currency",
        backref="currencies",
    )

    __table_args__ = (CheckConstraint("amount > 0", name="amount_positive"),)

    @staticmethod
    def from_entity(entity: TransactionEntity) -> "Transaction":
        return Transaction(
            transaction_id=entity.transaction_id,
            user_id=entity.user_id,
            category_id=entity.category.category_id,
            currency_id=entity.money.currency.currency_id,
            amount=entity.money.amount,
            description=entity.description,
            date=entity.date,
        )

    def to_entity(self) -> TransactionEntity:
        return TransactionEntity(
            transaction_id=self.transaction_id,
            user_id=self.user_id,
            category=self.category.to_entity(),
            money=Money(
                amount=self.amount,
                currency=self.currency.to_entity(),
            ),
            description=self.description,
            date=self.date,
        )
