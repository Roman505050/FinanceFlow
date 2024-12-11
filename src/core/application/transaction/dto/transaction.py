import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from core.domain.transaction.entities.transaction import TransactionEntity
from core.domain.transaction.enums.operation import OperationType


class CreateTransactionDTO(BaseModel):
    user_id: UUID
    category_id: UUID
    currency_id: UUID
    amount: Decimal = Field(gt=0, le=Decimal("99999999"))
    description: str | None = Field(min_length=10, max_length=255)
    date: datetime.datetime


class TransactionDTO(BaseModel):
    transaction_id: UUID
    user_id: UUID
    category_id: UUID
    category_name: str
    operation_id: UUID
    operation_name: str
    operation_type: OperationType
    currency_id: UUID
    currency_name: str
    currency_code: str
    currency_symbol: str
    amount: Decimal
    description: str | None
    date: datetime.datetime

    @staticmethod
    def from_entity(entity: TransactionEntity) -> "TransactionDTO":
        return TransactionDTO(
            transaction_id=entity.transaction_id,
            user_id=entity.user_id,
            category_id=entity.category.category_id,
            category_name=entity.category.category_name,
            operation_id=entity.category.operation.operation_id,
            operation_name=entity.category.operation.operation_name,
            operation_type=entity.category.operation.operation_type,
            currency_id=entity.money.currency.currency_id,
            currency_name=entity.money.currency.currency_name,
            currency_code=entity.money.currency.currency_code,
            currency_symbol=entity.money.currency.currency_symbol,
            amount=entity.money.amount,
            description=entity.description,
            date=entity.date,
        )
