from pydantic import BaseModel


class LoginInDTO(BaseModel):
    email: str
    password: str


class LoginOutDTO(BaseModel):
    access_token: str
    refresh_token: str

    @classmethod
    def from_domain(cls, access, refresh):
        return cls(access_token=access, refresh_token=refresh)
