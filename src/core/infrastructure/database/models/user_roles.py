from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
)
from uuid import uuid4, UUID

from core.infrastructure.database.models.base import (
    Base,
    created_at,
    updated_at,
)


class UserRoles(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey(
            "users.user_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    role_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey(
            "roles.role_id",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
