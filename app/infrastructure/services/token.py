from datetime import datetime, timedelta, timezone
import hashlib
from typing import Tuple
from uuid import UUID, uuid4

import jwt

from app.domain.contracts.auth.servicie import ITokenService
from app.domain.entities.auth import RefreshTokenEntity
from app.domain.exceptions.token import TokenExpiredException
from config import settings


class TokenService(ITokenService):
    def generate_access_token(self, user: UUID) -> str:
        payload = {
            'sub': str(user),
            'type': 'access',
            'exp': datetime.now(timezone.utc)
            + timedelta(minutes=int(settings.JWT_ACCESS_EXPIRE_MINUTES)),
        }
        return jwt.encode(
            payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

    def generate_refresh_token(
        self, user: UUID
    ) -> Tuple[str, RefreshTokenEntity]:
        raw_token = str(uuid4())

        hash_token = self.hash_token(raw_token)

        refresh = RefreshTokenEntity(
            token=hash_token,
            expired_at=datetime.now(timezone.utc)
            + timedelta(days=int(settings.JWT_REFRESH_EXPIRE_DAYS)),
        )

        return hash_token, refresh

    def hash_token(self, raw: str) -> str:
        return hashlib.sha256(raw.encode()).hexdigest()

    def decode_token(self, hash: str) -> dict:
        try:
            return jwt.decode(
                hash, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
