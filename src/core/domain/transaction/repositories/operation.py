from abc import ABC, abstractmethod
from uuid import UUID

from core.domain.transaction.entities.operation import OperationEntity


class IOperationRepository(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def save(self, operation: OperationEntity) -> OperationEntity: ...

    @abstractmethod
    async def get_by_id(self, operation_id: UUID) -> OperationEntity: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> OperationEntity: ...

    @abstractmethod
    async def get_all(self) -> list[OperationEntity]: ...
