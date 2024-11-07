from abc import ABC, abstractmethod


class ICryptographyService(ABC):
    @abstractmethod
    def generate_salt(self) -> str: ...

    @abstractmethod
    def hash_password(self, password: str, salt: str) -> str: ...

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool: ...
