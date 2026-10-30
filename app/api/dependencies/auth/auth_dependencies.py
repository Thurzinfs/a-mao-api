from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.user.user_dependencies import (
    get_hash_service,
    get_user_repository,
)
from app.application.use_cases.auth import (
    LoginUserUseCase,
    LogoutUserUseCase,
    RefreshTokenUserUseCase,
)
from app.domain.contracts.auth.repositorie import IRefreshTokenRepository
from app.domain.contracts.auth.servicie import ITokenService
from app.domain.contracts.user.hash import IHashService
from app.domain.contracts.user.repositorie import IUserRepository
from app.domain.entities.user import UserEntity
from app.infrastructure.database.repositories.auth import (
    AdvancedRefreshTokenRepository,
)
from app.infrastructure.database.sqlite.database import get_session
from app.infrastructure.services.token import TokenService
from config import settings


def get_token_repository(
    session: AsyncSession = Depends(get_session),
) -> IRefreshTokenRepository:
    return AdvancedRefreshTokenRepository(session=session)


def get_token_servicie() -> ITokenService:
    return TokenService()


def get_login_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
    token_repo: IRefreshTokenRepository = Depends(get_token_repository),
    token_service: ITokenService = Depends(get_token_servicie),
    hash_servicie: IHashService = Depends(get_hash_service),
) -> LoginUserUseCase:
    return LoginUserUseCase(
        user_repo=user_repo,
        token_repo=token_repo,
        token_service=token_service,
        hash_service=hash_servicie,
    )


def get_logout_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
    token_repo: IRefreshTokenRepository = Depends(get_token_repository),
) -> LogoutUserUseCase:
    return LogoutUserUseCase(user_repo=user_repo, token_repo=token_repo)


def get_refresh_token_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
    token_repo: IRefreshTokenRepository = Depends(get_token_repository),
    token_service: ITokenService = Depends(get_token_servicie),
    hash_servicie: IHashService = Depends(get_hash_service),
) -> RefreshTokenUserUseCase:
    return RefreshTokenUserUseCase(
        user_repo=user_repo,
        token_repo=token_repo,
        token_service=token_service,
        hash_service=hash_servicie,
    )


async def get_current_user(
    access_token: Annotated[
        str | None, Cookie(include_in_schema=False)
    ] = None,
    user_repo: IUserRepository = Depends(get_user_repository),
) -> UserEntity:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario não autenticado.',
        )

    token_str = (
        access_token.replace('Bearer ', '')
        if access_token.startswith('Bearer')
        else access_token
    )

    try:
        payload = jwt.decode(
            token_str, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get('type') != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Tipo de token invalido.',
            )
        user_id = payload.get('sub', '')

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalido ou expirado.',
        )

    user = await user_repo.find_by_id(user_id)

    if not user or user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario inativo ou nao encontrado.',
        )

    return user


LoginUserUseCaseDependency = Annotated[
    LoginUserUseCase, Depends(get_login_use_case)
]
LogoutUserUseCaseDependency = Annotated[
    LogoutUserUseCase, Depends(get_logout_use_case)
]
RefreshTokenUserUseCaseDependency = Annotated[
    RefreshTokenUserUseCase, Depends(get_refresh_token_use_case)
]
CurrentUserDependency = Annotated[UserEntity, Depends(get_current_user)]
