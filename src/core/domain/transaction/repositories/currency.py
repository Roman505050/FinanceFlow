from abc import ABC, abstractmethod
from uuid import UUID

from core.domain.transaction.entities.currency import CurrencyEntity


class ICurrencyRepository(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def save(self, currency: CurrencyEntity) -> CurrencyEntity: ...

    @abstractmethod
    async def get_by_id(self, currency_id: UUID) -> CurrencyEntity: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> CurrencyEntity: ...

    @abstractmethod
    async def get_all(self) -> list[CurrencyEntity]: ...
