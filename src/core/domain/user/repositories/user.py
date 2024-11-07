from abc import ABC, abstractmethod
from uuid import UUID

from core.domain.user.entities.user import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def save(self, user: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserEntity: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity: ...
