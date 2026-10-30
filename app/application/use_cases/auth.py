from uuid import UUID

from app.application.dtos.auth import LoginInDTO, LoginOutDTO
from app.domain.contracts.auth.repositorie import IRefreshTokenRepository
from app.domain.contracts.auth.servicie import ITokenService
from app.domain.contracts.user.hash import IHashService
from app.domain.contracts.user.repositorie import IUserRepository
from app.domain.exceptions.user import (
    CredentialsInvalidExcetion,
    UserNotFoundException,
)
from app.domain.exceptions.token import InvalidTokenException


class LoginUserUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        token_repo: IRefreshTokenRepository,
        token_service: ITokenService,
        hash_service: IHashService,
    ) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.token_service = token_service
        self.hash_service = hash_service

    async def execute(self, dto: LoginInDTO):
        user = await self.user_repo.find_by_email(dto.email)
        if not user:
            raise UserNotFoundException()

        if not self.hash_service.verify(dto.password, user.password):
            raise CredentialsInvalidExcetion()

        access_token = self.token_service.generate_access_token(user.id)

        refresh, entity = self.token_service.generate_refresh_token(user.id)

        await self.token_repo.save(entity)

        return LoginOutDTO.from_domain(access_token, refresh)


class LogoutUserUseCase:
    def __init__(
        self, user_repo: IUserRepository, token_repo: IRefreshTokenRepository
    ) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def execute(self, id: UUID):
        user = await self.user_repo.find_by_id(id)
        if not user:
            raise UserNotFoundException()

        if user.is_deleted():
            raise UserNotFoundException()

        tokens = await self.token_repo.list_tokens_by_user(user.id)
        for token in tokens:
            token.revoke()
            await self.token_repo.save(token)


class RefreshTokenUserUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        token_repo: IRefreshTokenRepository,
        token_service: ITokenService,
        hash_service: IHashService,
    ) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.token_service = token_service
        self.hash_service = hash_service

    async def execute(self, refresh: str):
        token = await self.token_repo.find_by_hash(refresh)
        if not token or not token.revoked or not token.is_valid():
            raise InvalidTokenException()

        if not token.user:
            raise UserNotFoundException()

        access_token = self.token_service.generate_access_token(token.user)

        new_refresh, entity = self.token_service.generate_refresh_token(
            token.user
        )

        token.revoke()
        await self.token_repo.save(token)
        await self.token_repo.save(entity)

        return LoginOutDTO.from_domain(access_token, new_refresh)
