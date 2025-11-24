from uuid import UUID

from litestar.exceptions import NotFoundException

from models import User
from repositories.user_repository import UserRepository
from schemas import UserDTO, UserAddDTO, UserUpdateDTO


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo


    async def get_user_by_id(self, user_id: UUID) -> UserDTO:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserDTO.model_validate(user, from_attributes=True)

