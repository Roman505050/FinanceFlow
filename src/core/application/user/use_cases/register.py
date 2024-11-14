from email_validator import validate_email, EmailNotValidError
from pydantic import ValidationError
from loguru import logger

from core.application.user.dto.user import RegisterUserDTO, UserDTO
from core.application.user.factories.user import UserFactory
from core.domain.user.entities.role import RoleEntity
from core.domain.user.exceptions import UserAlreadyExistsException
from core.domain.user.repositories.user import IUserRepository
from core.domain.user.repositories.role import IRoleRepository
from core.shared.exceptions import NotFoundException


class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        role_repository: IRoleRepository,
        user_factory: UserFactory,
    ):
        self._user_repository = user_repository
        self._user_factory = user_factory
        self._role_repository = role_repository

    async def execute(self, register_data: RegisterUserDTO) -> UserDTO:
        try:
            validate_email(register_data.email)
        except EmailNotValidError as e:
            raise ValueError("Invalid email") from e

        try:
            if await self._user_repository.get_by_username(
                register_data.username
            ):
                raise UserAlreadyExistsException(
                    f"Username {register_data.username} already exists"
                )
        except NotFoundException:
            pass

        try:
            if await self._user_repository.get_by_email(register_data.email):
                raise UserAlreadyExistsException(
                    f"Email {register_data.email} already exists"
                )
        except NotFoundException:
            pass

        try:
            member_role = await self._role_repository.get_by_name("member")
        except NotFoundException:
            logger.warning("Role 'member' not found, creating it")
            member_role = RoleEntity.create("member")

        user = self._user_factory.create_user(
            username=register_data.username,
            email=register_data.email,
            password=register_data.password.get_secret_value(),
            roles=[member_role],
        )

        user = await self._user_repository.save(user)

        try:
            user_dto = UserDTO.from_entity(user)
            return user_dto
        except ValidationError as e:
            # Because if an error occurs, it is not a user error
            logger.error(f"Error converting user {user.user_id!r} to DTO")
            raise Exception("Invalid data") from e
