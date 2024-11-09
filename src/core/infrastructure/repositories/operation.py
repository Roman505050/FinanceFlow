from sqlalchemy import select, delete, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


from core.domain.transaction.entities.operation import OperationEntity
from core.domain.transaction.exceptions.operation.already_exist import (
    OperationAlreadyExistException,
)
from core.domain.transaction.exceptions.operation.delete import (
    OperationNotDeletableException,
)
from core.domain.transaction.exceptions.operation.not_found import (
    OperationNotFoundException,
)
from core.domain.transaction.repositories.operation import IOperationRepository
from core.infrastructure.database.models.operation import Operation


class OperationRepository(IOperationRepository):
    model = Operation

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def save(self, operation: OperationEntity) -> OperationEntity:
        stmt = insert(self.model).values(
            operation_id=operation.operation_id,
            operation_name=operation.operation_name,
        )
        try:
            await self._session.execute(stmt)
        except IntegrityError:
            raise OperationAlreadyExistException(
                f"Operation with name {operation.operation_name!r} "
                f"already exists"
            )
        return operation

    async def get_by_id(self, operation_id: UUID) -> OperationEntity:
        stmt = select(self.model).filter_by(operation_id=operation_id)
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if not model_instance:
            raise OperationNotFoundException(
                f"Operation with id {operation_id!r} not found"
            )
        return model_instance.to_entity()

    async def get_all(self) -> list[OperationEntity]:
        stmt = select(self.model)
        result = await self._session.execute(stmt)
        model_instances = result.scalars().all()
        return [
            model_instance.to_entity() for model_instance in model_instances
        ]

    async def get_by_name(self, name: str) -> OperationEntity:
        stmt = select(self.model).filter_by(name=name)
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if not model_instance:
            raise OperationNotFoundException(
                f"Operation with name {name!r} not found"
            )
        return model_instance.to_entity()

    async def delete(self, operation_id: UUID) -> None:
        stmt = select(self.model).filter_by(operation_id=operation_id)
        result = await self._session.execute(stmt)
        model_instance = result.scalars().first()
        if not model_instance:
            raise OperationNotFoundException(
                f"Operation with id {str(operation_id)!r} not found"
            )

        stmt_delete = delete(self.model).filter_by(operation_id=operation_id)
        try:
            await self._session.execute(stmt_delete)
        except IntegrityError:
            raise OperationNotDeletableException(
                f"Operation with id {operation_id!r} cannot be deleted"
            )
