from pydantic import ValidationError
from loguru import logger
from uuid import UUID

from core.application.user.dto.user import UserDTO
from core.domain.user.repositories.user import IUserRepository


class GetUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def execute(self, user_id: UUID) -> UserDTO:
        user_entity = await self._user_repository.get_by_id(user_id)
        try:
            return UserDTO.from_entity(user_entity)
        except ValidationError as e:
            # Because if an error occurs, it is not a user error
            logger.error(f"Error converting user {user_id!r} to DTO")
            raise Exception("Error getting user") from e
