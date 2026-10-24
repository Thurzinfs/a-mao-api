from uuid import UUID

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.domain.entities.user import UserEntity
from app.domain.contracts.user_repositories import IUserRepository
from app.infrastructure.database.models.user import User


class AdvancedUserRepository(SQLAlchemyAsyncRepository[User], IUserRepository):
    model_type = User

    async def save(self, entity: UserEntity) -> UserEntity:
        model = self._entity_to_model(entity)
        saved_model = await self.upsert(model, auto_commit=True)
        return self._model_to_entity(saved_model)

    async def find_by_id(self, user: UUID) -> UserEntity | None:
        model = await self.get_one_or_none(id=user)
        if model is None:
            return None
        return self._model_to_entity(model)

    async def find_by_email(self, email: str) -> UserEntity | None:
        model = await self.get_one_or_none(email=email)
        if model is None:
            return None
        return self._model_to_entity(model)

    async def verify_email_exists(self, email: str) -> bool:
        model = await self.get_one_or_none(email=email)
        return model is not None

    def _entity_to_model(self, entity: UserEntity) -> User:
        return User(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            password=entity.password,
            deleted_at=entity.deleted_at,
        )

    def _model_to_entity(self, model: User) -> UserEntity:
        return UserEntity(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            deleted_at=model.deleted_at,
        )
