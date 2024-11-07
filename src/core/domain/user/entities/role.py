from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class RoleEntity:
    role_id: UUID
    role_name: str

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not 3 <= len(self.role_name) <= 64:
            raise ValueError("Role name must be between 3 and 64 characters")

    @staticmethod
    def create(role_name: str) -> "RoleEntity":
        return RoleEntity(role_id=uuid4(), role_name=role_name)
