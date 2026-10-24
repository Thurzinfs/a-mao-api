from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserInSchema(BaseModel):
    name: str
    email: str
    password: str

    def to_dto(self):
        from app.application.dtos.user import UserInDTO

        return UserInDTO(
            name=self.name, email=self.email, password=self.password
        )


class UserOutSchema(BaseModel):
    id: UUID
    name: str
    email: str

    @classmethod
    def from_dto(cls, dto):
        return cls(id=dto.id, name=dto.name, email=dto.email)


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    def to_dto(self):
        from app.application.dtos.user import UserUpdateDTO

        return UserUpdateDTO(name=self.name, email=self.email)
