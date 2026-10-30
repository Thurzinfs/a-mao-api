from abc import ABC, abstractmethod
from typing import Tuple
from uuid import UUID

from app.domain.entities.auth import RefreshTokenEntity


class ITokenService(ABC):
    @abstractmethod
    def generate_access_token(self, user: UUID) -> str:
        ...

    @abstractmethod
    def generate_refresh_token(
        self, user: UUID
    ) -> Tuple[str, RefreshTokenEntity]:
        ...

    @abstractmethod
    def hash_token(self, raw: str) -> str:
        ...

    @abstractmethod
    def decode_token(self, hash: str) -> dict:
        ...
