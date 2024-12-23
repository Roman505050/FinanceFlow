from loguru import logger
from pydantic import ValidationError

from core.application.user.dto.user import LoginUserDTO, UserDTO
from core.application.user.exceptions.invalid_credentials import (
    UserInvalidCredentialsException,
)
from core.application.user.ports.services.cryptography import (
    ICryptographyService,
)
from core.domain.user.repositories.user import IUserRepository
from core.shared.exceptions import NotFoundException


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        cryptography_service: ICryptographyService,
    ):
        self._user_repository = user_repository
        self._cryptography_service = cryptography_service

    async def execute(self, login_data: LoginUserDTO) -> UserDTO:
        try:
            user = await self._user_repository.get_by_email(login_data.email)
        except NotFoundException as e:
            raise UserInvalidCredentialsException(
                "Invalid email or password"
            ) from e

        if not self._cryptography_service.verify_password(
            password=login_data.password.get_secret_value(),
            hashed_password=user.password_hash,
        ):
            raise UserInvalidCredentialsException("Invalid email or password")

        try:
            return UserDTO.from_entity(user)
        except ValidationError as e:
            # Because if an error occurs, it is not a user error
            logger.error(f"Error converting user {user.user_id!r} to DTO")
            raise Exception("Invalid data") from e
