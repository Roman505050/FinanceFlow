from dataclasses import dataclass
from uuid import UUID

from core.domain.user.entities.role import RoleEntity


@dataclass
class UserEntity:
    user_id: UUID
    username: str
    email: str
    password_hash: str
    roles: list[RoleEntity]

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if len(self.email) > 100:
            raise ValueError("Email is too long")
        if not 3 <= len(self.username) <= 64:
            raise ValueError("Username must be between 3 and 64 characters")
