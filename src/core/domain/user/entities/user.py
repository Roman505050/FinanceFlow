from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class UserEntity:
    user_id: UUID
    username: str
    email: str
    password_hash: str

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if len(self.email) > 100:
            raise ValueError("Email is too long")
        if 3 > len(self.username) > 64:
            raise ValueError("Username must be between 3 and 64 characters")

    @staticmethod
    def create(username: str, email: str, password_hash: str) -> "UserEntity":
        return UserEntity(
            user_id=uuid4(),
            username=username,
            email=email,
            password_hash=password_hash,
        )
