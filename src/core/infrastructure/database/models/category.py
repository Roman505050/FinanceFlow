from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.domain.transaction.entities.category import CategoryEntity
from core.infrastructure.database.models.base import (
    Base,
    created_at,
    updated_at,
)
from core.infrastructure.database.models.operation import Operation


class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    operation_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey(
            "operations.operation_id",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    category_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    operation: Mapped[Operation] = relationship(
        "Operation",
        backref="categories",
    )

    __table_args__ = (UniqueConstraint("operation_id", "category_name"),)

    @staticmethod
    def from_entity(category: CategoryEntity) -> "Category":
        return Category(
            category_id=category.category_id,
            operation_id=category.operation.operation_id,
            category_name=category.category_name,
        )

    def to_entity(self) -> CategoryEntity:
        return CategoryEntity(
            category_id=self.category_id,
            operation=self.operation.to_entity(),
            category_name=self.category_name,
        )
