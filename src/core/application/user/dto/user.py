from pydantic import BaseModel, EmailStr, SecretStr, Field
from uuid import UUID


class LoginUserDTO(BaseModel):
    email: EmailStr = Field(max_length=100)
    password: SecretStr = Field(min_length=6, max_length=64)


class RegisterUserDTO(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr = Field(max_length=100)
    password: SecretStr = Field(min_length=6, max_length=64)


class UserDTO(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
