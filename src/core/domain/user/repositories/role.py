from abc import ABC, abstractmethod
from uuid import UUID

from core.domain.user.entities.role import RoleEntity


class IRoleRepository(ABC):
    @abstractmethod
    async def save(self, role: RoleEntity) -> RoleEntity: ...

    @abstractmethod
    async def delete(self, role_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, role_id: UUID) -> RoleEntity: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> RoleEntity: ...
