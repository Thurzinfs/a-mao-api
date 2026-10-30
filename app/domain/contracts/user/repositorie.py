from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.user import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: UserEntity) -> None:
        ...

    @abstractmethod
    async def find_by_id(self, user: UUID) -> UserEntity | None:
        ...

    @abstractmethod
    async def find_by_email(self, email: str) -> UserEntity | None:
        ...

    @abstractmethod
    async def verify_email_exists(self, email: str) -> bool:
        ...
