from typing import Optional
from uuid import UUID

from litestar.exceptions import NotFoundException

from models import User
from repositories.user_repository import UserRepository
from schemas import UserDTO, UserAddDTO, UserUpdateDTO


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_by_id(self, user_id: UUID) -> UserDTO:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserDTO.model_validate(user)

    async def create(self, user_data: UserAddDTO) -> UserDTO:
        user = await self.user_repo.create(user_data)
        return UserDTO.model_validate(user)

    async def delete(self, user_id: UUID) -> UserDTO:
        user = await self.user_repo.delete(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserDTO.model_validate(user)

    async def update(self, user_id: UUID, user_data: UserUpdateDTO) -> User:
        user = await self.user_repo.update(user_id, user_data)
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        return UserDTO.model_validate(user)
    
    async def get_user_count(self) -> int:
        return await self.user_repo.get_user_count()

    async def get_by_filter(self, count: Optional[int] = None, page: int = 1, **kwargs) -> list[UserDTO]:
        users = await self.user_repo.get_by_filter(count, page, **kwargs)
        user_dtos = [UserDTO.model_validate(user) for user in users]
        return user_dtos
