from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class RefreshTokenEntity:
    id: UUID = field(default_factory=uuid4)
    user: UUID | None = field(default=None)
    token: str = field(default='')
    expired_at: datetime | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    revoked: bool = field(default=False)

    def is_valid(self) -> bool:
        if self.revoked:
            return False
        if self.expired_at and datetime.now() > self.expired_at:
            return False
        return True

    def revoke(self) -> None:
        self.revoked = True
