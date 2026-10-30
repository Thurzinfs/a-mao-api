from pydantic import BaseModel, EmailStr

from app.application.dtos.auth import LoginInDTO


class LoginInSchema(BaseModel):
    email: EmailStr
    password: str

    def to_dto(self) -> LoginInDTO:
        return LoginInDTO(email=str(self.email), password=self.password)
