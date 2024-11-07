from uuid import uuid4

from core.application.user.ports.services.cryptography import (
    ICryptographyService,
)
from core.domain.user.entities.role import RoleEntity
from core.domain.user.entities.user import UserEntity


class UserFactory:
    def __init__(self, cryptography_service: ICryptographyService):
        self._cryptography_service = cryptography_service

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        roles: list[RoleEntity],
    ) -> UserEntity:
        salt = self._cryptography_service.generate_salt()
        password_hash = self._cryptography_service.hash_password(
            password=password, salt=salt
        )
        return UserEntity(
            user_id=uuid4(),
            username=username,
            email=email,
            password_hash=password_hash,
            roles=roles,
        )
