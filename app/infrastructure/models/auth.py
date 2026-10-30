from datetime import datetime
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.models.user import User


class RefreshToken(UUIDAuditBase):
    __tablename__ = 'refresh_tokens'

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id'), nullable=True
    )
    user: Mapped['User'] = relationship('User', lazy='joined')
    token: Mapped[str] = mapped_column(nullable=False)
    expired_at: Mapped[datetime]
    revoked: Mapped[bool] = mapped_column(default=False)
