from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, SecretStr

from core.application.user.dto.role import RoleDTO
from core.domain.user.entities.user import UserEntity


class LoginUserDTO(BaseModel):
    email: EmailStr = Field(max_length=100)
    password: SecretStr = Field(min_length=6, max_length=64)


class RegisterUserDTO(BaseModel):
    username: str = Field(
        min_length=3, max_length=64, pattern=r"^[a-zA-Z0-9_]*$"
    )
    email: EmailStr = Field(max_length=100)
    password: SecretStr = Field(min_length=6, max_length=64)


class UserDTO(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    roles: list[RoleDTO]

    @staticmethod
    def from_entity(entity: UserEntity) -> "UserDTO":
        return UserDTO(
            user_id=entity.user_id,
            username=entity.username,
            email=entity.email,
            roles=[RoleDTO.from_entity(role) for role in entity.roles],
        )
