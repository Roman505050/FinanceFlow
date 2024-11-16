from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
)
from uuid import uuid4, UUID

from core.domain.transaction.entities.currency import CurrencyEntity
from core.infrastructure.database.models.base import (
    Base,
    created_at,
    updated_at,
)


class Currency(Base):
    __tablename__ = "currencies"

    currency_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    currency_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    currency_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        unique=True,
        index=True,
    )
    currency_symbol: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    def from_entity(currency: CurrencyEntity) -> "Currency":
        return Currency(
            currency_id=currency.currency_id,
            currency_name=currency.currency_name,
            currency_code=currency.currency_code,
            currency_symbol=currency.currency_symbol,
        )

    def to_entity(self) -> CurrencyEntity:
        return CurrencyEntity(
            currency_id=self.currency_id,
            currency_name=self.currency_name,
            currency_code=self.currency_code,
            currency_symbol=self.currency_symbol,
        )
