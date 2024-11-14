from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.domain.user.entities.role import RoleEntity
from core.domain.user.repositories.role import IRoleRepository
from core.domain.user.exceptions import RoleNotFoundException
from core.infrastructure.database.models.role import Role


class RoleRepository(IRoleRepository):
    model = Role

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, role: RoleEntity) -> RoleEntity:
        role_model = self.model.from_entity(role)
        self._session.add(role_model)
        await self._session.commit()
        return role_model.to_entity()

    async def delete(self, role_id: UUID) -> None:
        stmt = delete(self.model).filter_by(role_id=role_id)
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            raise RoleNotFoundException(f"Role with id {role_id} not found")
        await self._session.commit()

    async def get_by_id(self, role_id: UUID) -> RoleEntity:
        stmt = select(self.model).filter_by(role_id=role_id)
        result = await self._session.execute(stmt)
        role_model = result.scalar()
        if role_model is None:
            raise RoleNotFoundException(f"Role with id {role_id} not found")
        return role_model.to_entity()

    async def get_by_name(self, name: str) -> RoleEntity:
        stmt = select(self.model).filter_by(role_name=name)
        result = await self._session.execute(stmt)
        role_model = result.scalar()
        if role_model is None:
            raise RoleNotFoundException(f"Role with name {name} not found")
        return role_model.to_entity()
