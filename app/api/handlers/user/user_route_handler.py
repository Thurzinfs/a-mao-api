from uuid import UUID

from fastapi import APIRouter, FastAPI
from pydantic import EmailStr

from app.api.dependencies.user.user_dependencies import (
    GetUserByEmailUseCaseDependency,
    RegisterUserUseCaseDependency,
    GetUserByIDUseCaseDependency,
    UpdateUserUseCaseDependency,
    DeleteUserUseCaseDependency,
)
from app.api.schemas.user.user_schemas import (
    UserInSchema,
    UserOutSchema,
    UserUpdateSchema,
)


class UserAPIRouteHandler:
    def __init__(self) -> None:
        self.router = APIRouter(prefix='/users', tags=['Users'])

        self._register_user_post_route()
        self._register_get_user_by_id_route()
        self._register_get_user_by_email_route()
        self._register_update_user_route()
        self._register_delete_user_route()

    def register_route(self, app: FastAPI) -> None:
        app.include_router(self.router)

    def _register_user_post_route(self) -> None:
        @self.router.post('/', response_model=UserOutSchema)
        async def register_user(
            data: UserInSchema, use_case: RegisterUserUseCaseDependency
        ):
            dto = data.to_dto()

            user = await use_case.execute(dto)
            return UserOutSchema.from_dto(user)

    def _register_get_user_by_id_route(self) -> None:
        @self.router.get('/{user_id}', response_model=UserOutSchema)
        async def get_user(id: UUID, use_case: GetUserByIDUseCaseDependency):
            user = await use_case.execute(id)
            return UserOutSchema.from_dto(user)

    def _register_get_user_by_email_route(self) -> None:
        @self.router.get('/email/{email}', response_model=UserOutSchema)
        async def get_user_by_email(
            email: EmailStr, use_case: GetUserByEmailUseCaseDependency
        ):
            user = await use_case.execute(str(email))
            return UserOutSchema.from_dto(user)

    def _register_update_user_route(self) -> None:
        @self.router.put('/{id}', response_model=UserOutSchema)
        async def update_user(
            id: UUID,
            data: UserUpdateSchema,
            use_case: UpdateUserUseCaseDependency,
        ):
            dto = data.to_dto()
            user = await use_case.execute(id, dto)
            return UserOutSchema.from_dto(user)

    def _register_delete_user_route(self) -> None:
        @self.router.delete('/{id}', response_model=None)
        async def delete_user(id: UUID, use_case: DeleteUserUseCaseDependency):
            await use_case.execute(id)
            return 'User deleted successfully'
