from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.domain.transaction.entities.transaction import TransactionEntity
from core.domain.transaction.exceptions.transaction.not_found import (
    TransactionNotFoundException,
)
from core.domain.transaction.filters.transaction import TransactionFilters
from core.domain.transaction.repositories.transaction import (
    ITransactionRepository,
)
from core.infrastructure.database.models.category import Category
from core.infrastructure.database.models.transaction import Transaction


class TransactionRepository(ITransactionRepository):
    model = Transaction

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, transaction: TransactionEntity) -> TransactionEntity:
        stmt = insert(self.model).values(
            transaction_id=transaction.transaction_id,
            user_id=transaction.user_id,
            category_id=transaction.category.category_id,
            currency_id=transaction.money.currency.currency_id,
            amount=transaction.money.amount,
            date=transaction.date,
            description=transaction.description,
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return transaction

    async def delete(self, transaction_id: UUID) -> None:
        stmt = select(self.model).filter_by(transaction_id=transaction_id)
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if model_instance is None:
            raise TransactionNotFoundException(
                f"Transaction with id {str(transaction_id)!r} not found"
            )

        stmt_delete = delete(self.model).where(
            self.model.transaction_id == transaction_id
        )
        await self._session.execute(stmt_delete)
        await self._session.commit()

    async def get_by_id(self, transaction_id: UUID) -> TransactionEntity:
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.category).options(
                    selectinload(Category.operation)
                )
            )
            .options(selectinload(self.model.currency))
            .filter_by(transaction_id=transaction_id)
        )
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if model_instance is None:
            raise TransactionNotFoundException(
                f"Transaction with id {str(transaction_id)!r} not found"
            )
        return model_instance.to_entity()

    async def get_by_filters(
        self, filters: TransactionFilters
    ) -> list[TransactionEntity]:
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.category).options(
                    selectinload(Category.operation)
                )
            )
            .options(selectinload(self.model.currency))
        )
        if filters.user_id:
            stmt = stmt.filter_by(user_id=filters.user_id)
        if filters.currency_ids:
            if len(filters.currency_ids) > 1:
                stmt = stmt.filter(
                    self.model.currency_id.in_(filters.currency_ids)
                )
            else:
                stmt = stmt.filter_by(currency_id=filters.currency_ids[0])
        if filters.currency_ids:
            if len(filters.currency_ids) > 1:
                stmt = stmt.filter(
                    self.model.currency_id.in_(filters.currency_ids)
                )
            else:
                stmt = stmt.filter_by(currency_id=filters.currency_ids[0])
        if filters.category_ids:
            if len(filters.category_ids) > 1:
                stmt = stmt.filter(
                    self.model.category_id.in_(filters.category_ids)
                )
            else:
                stmt = stmt.filter_by(category_id=filters.category_ids[0])
        if filters.data_range:
            stmt = stmt.filter(
                self.model.date >= filters.data_range.start_date,
                self.model.date <= filters.data_range.end_date,
            )
        if filters.amount_range:
            stmt = stmt.filter(
                self.model.amount >= filters.amount_range.min_amount,
                self.model.amount <= filters.amount_range.max_amount,
            )
        result = await self._session.execute(stmt)
        return [model.to_entity() for model in result.scalars()]

    async def update(
        self, transaction: TransactionEntity
    ) -> TransactionEntity:
        stmt = select(self.model).filter_by(
            transaction_id=transaction.transaction_id
        )
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if model_instance is None:
            raise TransactionNotFoundException(
                f"Transaction with id "
                f"{str(transaction.transaction_id)!r} not found"
            )
        stmt_update = (
            update(self.model)
            .where(self.model.transaction_id == transaction.transaction_id)
            .values(
                category_id=transaction.category.category_id,
                currency_id=transaction.money.currency.currency_id,
                date=transaction.date,
                amount=transaction.money.amount,
                description=transaction.description,
            )
        )
        await self._session.execute(stmt_update)
        await self._session.commit()
        return model_instance.to_entity()
