from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.user import (
    DeleteUserByIDUseCase,
    GetUserByEmailUseCase,
    GetUserByIDUseCase,
    RegisterUserUseCase,
    UpdateUserUseCase,
)
from app.domain.contracts.hash_service import IHashService
from app.domain.contracts.user_repositories import IUserRepository
from app.infrastructure.database.repositories.user import (
    AdvancedUserRepository,
)
from app.infrastructure.database.sqlite.database import get_session
from app.infrastructure.services.user import HashService


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> IUserRepository:
    return AdvancedUserRepository(session=session)


def get_hash_service() -> IHashService:
    return HashService()


def get_user_use_cases(
    user_repo: IUserRepository = Depends(get_user_repository),
    hash_service: IHashService = Depends(get_hash_service),
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repo, hash_service)


def get_user_by_id_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
) -> GetUserByIDUseCase:
    return GetUserByIDUseCase(user_repo)


def get_user_by_email_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
) -> GetUserByEmailUseCase:
    return GetUserByEmailUseCase(user_repo)


def get_update_user_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repo)


def delete_user_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
) -> DeleteUserByIDUseCase:
    return DeleteUserByIDUseCase(user_repo)


RegisterUserUseCaseDependency = Annotated[
    RegisterUserUseCase, Depends(get_user_use_cases)
]
GetUserByIDUseCaseDependency = Annotated[
    GetUserByIDUseCase, Depends(get_user_by_id_use_case)
]
GetUserByEmailUseCaseDependency = Annotated[
    GetUserByEmailUseCase, Depends(get_user_by_email_use_case)
]
UpdateUserUseCaseDependency = Annotated[
    UpdateUserUseCase, Depends(get_update_user_use_case)
]
DeleteUserUseCaseDependency = Annotated[
    DeleteUserByIDUseCase, Depends(delete_user_use_case)
]
