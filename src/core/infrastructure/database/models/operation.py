from sqlalchemy import String, CheckConstraint, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
)
from uuid import uuid4, UUID

from core.domain.transaction.entities.operation import OperationEntity
from core.domain.transaction.enums.operation import OperationType
from core.infrastructure.database.models.base import (
    Base,
    created_at,
    updated_at,
)


class Operation(Base):
    __tablename__ = "operations"

    operation_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    operation_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )
    operation_type: Mapped[OperationType] = mapped_column(
        SmallInteger,
        nullable=False,
        comment="0 - income, 1 - expense, 2 - investment",
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    __table_args__ = (
        CheckConstraint(
            "operation_type IN (0, 1, 2)", name="operation_type_check"
        ),
    )

    @staticmethod
    def from_entity(operation: OperationEntity) -> "Operation":
        return Operation(
            operation_id=operation.operation_id,
            operation_name=operation.operation_name,
            operation_type=operation.operation_type.value,
        )

    def to_entity(self) -> OperationEntity:
        return OperationEntity(
            operation_id=self.operation_id,
            operation_name=self.operation_name,
            operation_type=OperationType(self.operation_type),
        )
