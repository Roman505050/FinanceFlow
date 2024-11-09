from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
)
from uuid import uuid4, UUID

from core.domain.transaction.entities.operation import OperationEntity
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
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    def from_entity(operation: OperationEntity) -> "Operation":
        return Operation(
            operation_id=operation.operation_id,
            operation_name=operation.operation_name,
        )

    def to_entity(self) -> OperationEntity:
        return OperationEntity(
            operation_id=self.operation_id,
            operation_name=self.operation_name,
        )
