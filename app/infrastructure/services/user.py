from passlib.context import CryptContext

from app.domain.contracts.hash_service import IHashService


class HashService(IHashService):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"])
        
    def hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
