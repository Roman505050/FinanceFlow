from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.transaction.entities.currency import CurrencyEntity
from core.domain.transaction.exceptions import (
    CategoryNotDeletableException,
    CurrencyAlreadyExistException,
    CurrencyNotFoundException,
)
from core.domain.transaction.repositories.currency import ICurrencyRepository
from core.infrastructure.database.models.currency import Currency


class CurrencyRepository(ICurrencyRepository):
    model = Currency

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, currency: CurrencyEntity) -> CurrencyEntity:
        stmt = insert(self.model).values(
            currency_id=currency.currency_id,
            currency_code=currency.currency_code,
            currency_name=currency.currency_name,
            currency_symbol=currency.currency_symbol,
        )
        try:
            await self._session.execute(stmt)
        except IntegrityError as e:
            raise CurrencyAlreadyExistException(
                f"Currency with code {currency.currency_code!r} "
                f"already exists"
            ) from e
        await self._session.commit()
        return currency

    async def get_by_id(self, currency_id: UUID) -> CurrencyEntity:
        stmt = select(self.model).filter_by(currency_id=currency_id)
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if not model_instance:
            raise CurrencyNotFoundException(
                f"Currency with id {currency_id!r} not found"
            )
        return model_instance.to_entity()

    async def get_all(self) -> list[CurrencyEntity]:
        stmt = select(self.model)
        result = await self._session.execute(stmt)
        return [model.to_entity() for model in result.scalars()]

    async def get_by_name(self, name: str) -> CurrencyEntity:
        stmt = select(self.model).filter_by(currency_name=name)
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if not model_instance:
            raise CurrencyNotFoundException(
                f"Currency with name {name!r} not found"
            )
        return model_instance.to_entity()

    async def delete(self, currency_id: UUID) -> None:
        stmt = select(self.model).filter_by(currency_id=currency_id)
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if not model_instance:
            raise CurrencyNotFoundException(
                f"Category with id {str(currency_id)!r} not found"
            )

        stmt_delete = delete(self.model).filter_by(currency_id=currency_id)
        try:
            await self._session.execute(stmt_delete)
        except IntegrityError as e:
            raise CategoryNotDeletableException(
                f"Category with id {str(currency_id)!r} not deletable"
            ) from e
        await self._session.commit()
