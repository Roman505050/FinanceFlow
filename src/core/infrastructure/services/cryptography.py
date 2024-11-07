import bcrypt

from core.application.user.ports.services.cryptography import (
    ICryptographyService,
)


class CryptographyService(ICryptographyService):
    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode("utf-8")

    def hash_password(self, password: str, salt: str) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"), salt.encode("utf-8")
        ).decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )
