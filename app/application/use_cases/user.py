from uuid import UUID

from app.application.dtos.user import UserInDTO, UserOutDTO, UserUpdateDTO
from app.domain.contracts.hash_service import IHashService
from app.domain.contracts.user_repositories import IUserRepository
from app.domain.entities.user import UserEntity
from app.domain.exceptions.user import UserAlreadyExistsException, UserNotFoundException


class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository, hash_service: IHashService):
        self.user_repo = user_repo
        self.hash_service = hash_service

    async def execute(self, dto: UserInDTO):
        if await self.user_repo.verify_email_exists(dto.email):
            raise UserAlreadyExistsException()

        password_hash = self.hash_service.hash(dto.password)

        user = UserEntity(
            name=dto.name,
            email=dto.email,
            password=password_hash
        )

        await self.user_repo.save(user)

        return UserOutDTO.from_entity(user)


class GetUserByIDUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user: UUID):
        entity = await self.user_repo.find_by_id(user)
        if not entity:
            raise UserNotFoundException()

        return UserOutDTO.from_entity(entity)


class GetUserByEmailUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, email: str):
        user = await self.user_repo.find_by_email(email)
        if not user:
            raise UserNotFoundException()

        return UserOutDTO.from_entity(user)


class UpdateUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user: UUID, dto: UserUpdateDTO):
        entity = await self.user_repo.find_by_id(user)
        if not entity:
            raise UserNotFoundException()

        if dto.name:
            entity.change_name(dto.name)

        if dto.email:
            if await self.user_repo.verify_email_exists(dto.email):
                raise UserAlreadyExistsException()
                
            entity.change_email(dto.email)

        await self.user_repo.save(entity)

        return UserOutDTO.from_entity(entity)


class DeleteUserByIDUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user: UUID):
        entity = await self.user_repo.find_by_id(user)
        if not entity:
            raise UserNotFoundException()

        entity.delete()

        await self.user_repo.save(entity)
