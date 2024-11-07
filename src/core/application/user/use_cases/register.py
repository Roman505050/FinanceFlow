from email_validator import validate_email, EmailNotValidError
from pydantic import ValidationError

from core.application.user.dto.user import RegisterUserDTO, UserDTO
from core.application.user.ports.services.cryptography import (
    ICryptographyService,
)
from core.domain.user.repositories.exceptions import UserAlreadyExistsException
from core.domain.user.repositories.user import IUserRepository
from core.domain.user.entities.user import UserEntity
from core.shared.exceptions import NotFoundException


class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        cryptography_service: ICryptographyService,
    ):
        self._user_repository = user_repository
        self._cryptography_service = cryptography_service

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

        salt = self._cryptography_service.generate_salt()
        password_hash = self._cryptography_service.hash_password(
            password=register_data.password.get_secret_value(), salt=salt
        )

        user = UserEntity.create(
            username=register_data.username,
            email=register_data.email,
            password_hash=password_hash,
        )

        await self._user_repository.save(user)
        try:
            user_dto = UserDTO(
                user_id=user.user_id, username=user.username, email=user.email
            )
            await self._user_repository.commit()
            return user_dto
        except ValidationError as e:
            # Because if an error occurs, it is not a user error
            print(e)  # TODO: replace with logger
            raise Exception("Invalid data") from e
