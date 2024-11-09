from abc import ABC, abstractmethod
from uuid import UUID

from core.domain.transaction.entities.transaction import TransactionEntity
from core.domain.transaction.filters.transaction import TransactionFilters


class ITransactionRepository(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def save(
        self, transaction: TransactionEntity
    ) -> TransactionEntity: ...

    @abstractmethod
    async def delete(self, transaction_id: UUID) -> None: ...

    @abstractmethod
    async def update(
        self, transaction: TransactionEntity
    ) -> TransactionEntity: ...

    @abstractmethod
    async def get_by_id(self, transaction_id: UUID) -> TransactionEntity: ...

    @abstractmethod
    async def get_by_filters(
        self, filters: TransactionFilters
    ) -> list[TransactionEntity]: ...
