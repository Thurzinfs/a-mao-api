from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserInDTO(BaseModel):
    name: str
    email: str
    password: str


class UserOutDTO(BaseModel):
    id: UUID
    name: str
    email: str

    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            name=user.name,
            email=user.email
        )


class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
