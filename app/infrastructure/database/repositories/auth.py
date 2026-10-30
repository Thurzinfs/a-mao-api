from typing import List
from uuid import UUID

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.domain.contracts.auth.repositorie import IRefreshTokenRepository
from app.domain.entities.auth import RefreshTokenEntity
from app.infrastructure.models.auth import RefreshToken


class AdvancedRefreshTokenRepository(
    SQLAlchemyAsyncRepository[RefreshToken], IRefreshTokenRepository
):
    model_type = RefreshToken

    async def save(self, entity: RefreshTokenEntity) -> RefreshTokenEntity:
        model = self._entity_to_model(entity)
        saved_model = await self.upsert(model, auto_commit=True)
        return self._model_to_entity(saved_model)

    async def find_by_hash(self, hash: str) -> RefreshTokenEntity | None:
        model = await self.get_one_or_none(token=hash)
        if not model:
            return None

        return self._model_to_entity(model)

    async def list_tokens_by_user(
        self, user: UUID
    ) -> List[RefreshTokenEntity]:
        models = await self.list(user_id=user)
        return [self._model_to_entity(model) for model in models]

    def _entity_to_model(self, entity: RefreshTokenEntity) -> RefreshToken:
        return RefreshToken(
            id=entity.id,
            user_id=entity.user,
            token=entity.token,
            expired_at=entity.expired_at,
            revoked=entity.revoked,
            created_at=entity.created_at,
        )

    def _model_to_entity(self, model: RefreshToken) -> RefreshTokenEntity:
        return RefreshTokenEntity(
            id=model.id,
            user=model.user_id,
            token=model.token,
            expired_at=model.expired_at,
            revoked=model.revoked,
            created_at=model.created_at,
        )
