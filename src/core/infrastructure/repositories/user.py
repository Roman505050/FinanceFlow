from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.infrastructure.database.models.user import User
from core.domain.user.entities.user import UserEntity
from core.domain.user.repositories.exceptions import UserNotFoundException
from core.domain.user.repositories.user import IUserRepository


class UserRepository(IUserRepository):
    model = User

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def save(self, user: UserEntity) -> UserEntity:
        user_model = self.model.from_entity(user)
        self._session.add(user_model)
        return user_model.to_entity()

    async def delete(self, user_id: UUID) -> None:
        stmt = delete(self.model).filter_by(user_id=user_id)
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            raise UserNotFoundException(f"User with id {user_id} not found")

    async def get_by_id(self, user_id: UUID) -> UserEntity:
        stmt = select(self.model).filter_by(user_id=user_id)
        result = await self._session.execute(stmt)
        user_model = result.scalar()
        if user_model is None:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return user_model.to_entity()

    async def get_by_username(self, username: str) -> UserEntity:
        stmt = select(self.model).filter_by(username=username)
        result = await self._session.execute(stmt)
        user_model = result.scalar()
        if user_model is None:
            raise UserNotFoundException(
                f"User with username {username} not found"
            )
        return user_model.to_entity()

    async def get_by_email(self, email: str) -> UserEntity:
        stmt = select(self.model).filter_by(email=email)
        result = await self._session.execute(stmt)
        user_model = result.scalar()
        if user_model is None:
            raise UserNotFoundException(f"User with email {email} not found")
        return user_model.to_entity()
