from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
)
from uuid import uuid4, UUID
import asyncio

from core.domain.user.entities.user import UserEntity
from core.infrastructure.database.models.role import Role
from core.infrastructure.database.models.base import (
    Base,
    created_at,
    updated_at,
)


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    roles: Mapped[list[Role]] = relationship(
        "Role",
        secondary="user_roles",
        backref="users",
    )

    @staticmethod
    def from_entity(user: UserEntity) -> "User":
        return User(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
        )

    def to_entity(self) -> UserEntity:
        return UserEntity(
            user_id=self.user_id,
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
            roles=[role.to_entity() for role in self.roles],
        )
