from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.domain.transaction.entities.category import CategoryEntity
from core.domain.transaction.exceptions.category.already_exist import (
    CategoryAlreadyExistException,
)
from core.domain.transaction.exceptions.category.delete import (
    CategoryNotDeletableException,
)
from core.domain.transaction.exceptions.category.not_found import (
    CategoryNotFoundException,
)
from core.domain.transaction.repositories.category import ICategoryRepository
from core.infrastructure.database.models.category import Category


class CategoryRepository(ICategoryRepository):
    model = Category

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, category: CategoryEntity) -> CategoryEntity:
        stmt = insert(self.model).values(
            category_id=category.category_id,
            category_name=category.category_name,
            operation_id=category.operation.operation_id,
        )
        try:
            await self._session.execute(stmt)
        except IntegrityError as e:
            raise CategoryAlreadyExistException(
                f"Category with name {category.category_name!r} "
                f"already exists for "
                f"operation {category.operation.operation_name!r}"
            ) from e
        await self._session.commit()
        return category

    async def get_by_id(self, category_id: UUID) -> CategoryEntity:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.operation))
            .filter_by(category_id=category_id)
        )
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if not model_instance:
            raise CategoryNotFoundException(
                f"Category with id {str(category_id)!r} not found"
            )
        return model_instance.to_entity()

    async def get_by_operation_id(
        self, operation_id: UUID
    ) -> list[CategoryEntity]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.operation))
            .filter_by(operation_id=operation_id)
        )
        result = await self._session.execute(stmt)
        model_instances = result.scalars().all()
        return [
            model_instance.to_entity() for model_instance in model_instances
        ]

    async def get_all(self) -> list[CategoryEntity]:
        stmt = select(self.model).options(selectinload(self.model.operation))
        result = await self._session.execute(stmt)
        model_instances = result.scalars().all()
        return [
            model_instance.to_entity() for model_instance in model_instances
        ]

    async def get_by_name(self, name: str) -> CategoryEntity:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.operation))
            .filter_by(name=name)
        )
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if not model_instance:
            raise CategoryNotFoundException(
                f"Category with name {name!r} not found"
            )
        return model_instance.to_entity()

    async def delete(self, category_id: UUID) -> None:
        stmt = select(self.model).filter_by(category_id=category_id)
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if not model_instance:
            raise CategoryNotFoundException(
                f"Category with id {str(category_id)!r} not found"
            )
        stmt_delete = delete(self.model).filter_by(category_id=category_id)

        try:
            await self._session.execute(stmt_delete)
        except IntegrityError as e:
            raise CategoryNotDeletableException(
                f"Category with id {str(category_id)!r} not deletable"
            ) from e
        await self._session.commit()
