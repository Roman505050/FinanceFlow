from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
)
from uuid import uuid4, UUID

from core.domain.user.entities.role import RoleEntity
from core.infrastructure.database.models.base import (
    Base,
    created_at,
    updated_at,
)


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    role_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    def from_entity(role: RoleEntity) -> "Role":
        return Role(
            role_id=role.role_id,
            role_name=role.role_name,
        )

    def to_entity(self) -> RoleEntity:
        return RoleEntity(
            role_id=self.role_id,
            role_name=self.role_name,
        )
