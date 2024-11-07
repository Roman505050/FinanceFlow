from sqlalchemy import delete, select, insert, text
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.infrastructure.database.models.user import User
from core.infrastructure.database.models.role import Role
from core.domain.user.entities.user import UserEntity
from core.domain.user.exceptions import UserNotFoundException
from core.domain.user.repositories.user import IUserRepository
from core.infrastructure.database.models.user_roles import UserRoles


class UserRepository(IUserRepository):
    model = User

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def save(self, user: UserEntity) -> UserEntity:
        user_model = self.model.from_entity(user)
        await self._session.execute(
            insert(self.model).values(
                user_id=user_model.user_id,
                username=user_model.username,
                email=user_model.email,
                password_hash=user_model.password_hash,
            )
        )

        for role in user.roles:
            stmt_insert_role = """
                INSERT INTO roles (role_id, role_name, created_at, updated_at)
                VALUES (:role_id, :role_name, now(), now())
                ON CONFLICT (role_name) DO NOTHING;
            """

            await self._session.execute(
                text(stmt_insert_role),
                {"role_id": role.role_id, "role_name": role.role_name},
            )

            result = await self._session.execute(
                select(Role).filter_by(role_name=role.role_name)
            )
            role_model = result.scalar_one_or_none()

            if role_model:
                await self._session.execute(
                    insert(UserRoles).values(
                        role_id=role_model.role_id, user_id=user_model.user_id
                    )
                )

        # Load roles to user model
        roles_result = await self._session.execute(
            select(Role).join(UserRoles).filter_by(user_id=user_model.user_id)
        )
        roles = roles_result.scalars().all()
        user_model.roles = list(roles)

        return user_model.to_entity()

    async def delete(self, user_id: UUID) -> None:
        stmt = delete(self.model).filter_by(user_id=user_id)
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            raise UserNotFoundException(f"User with id {user_id} not found")

    async def get_by_id(self, user_id: UUID) -> UserEntity:
        stmt = (
            select(self.model)
            .options(selectinload(User.roles))
            .filter_by(user_id=user_id)
        )
        result = await self._session.execute(stmt)
        user_model = result.scalar()
        if user_model is None:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return user_model.to_entity()

    async def get_by_username(self, username: str) -> UserEntity:
        stmt = (
            select(self.model)
            .options(selectinload(User.roles))
            .filter_by(username=username)
        )
        result = await self._session.execute(stmt)
        user_model = result.scalar()
        if user_model is None:
            raise UserNotFoundException(
                f"User with username {username} not found"
            )
        return user_model.to_entity()

    async def get_by_email(self, email: str) -> UserEntity:
        stmt = (
            select(self.model)
            .options(selectinload(User.roles))
            .filter_by(email=email)
        )
        result = await self._session.execute(stmt)
        user_model = result.scalar()
        if user_model is None:
            raise UserNotFoundException(f"User with email {email} not found")
        return user_model.to_entity()
