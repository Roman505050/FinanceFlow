from abc import ABC, abstractmethod
from uuid import UUID

from core.domain.transaction.entities.category import CategoryEntity


class ICategoryRepository(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def save(self, category: CategoryEntity) -> CategoryEntity: ...

    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> CategoryEntity: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> CategoryEntity: ...

    @abstractmethod
    async def get_all(self) -> list[CategoryEntity]: ...

    @abstractmethod
    async def get_by_operation_id(
        self, operation_id: UUID
    ) -> list[CategoryEntity]: ...

    @abstractmethod
    async def delete(self, category_id: UUID) -> None: ...
