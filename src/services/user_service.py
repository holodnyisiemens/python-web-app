from typing import Optional
from uuid import UUID

from litestar.exceptions import NotFoundException, HTTPException

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
        try:
            user = await self.user_repo.create(user_data)
            await self.user_repo.session.commit()
        except:
            await self.user_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"User create error")
    
        return UserDTO.model_validate(user)

    async def delete(self, user_id: UUID) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

        try:
            await self.user_repo.delete(user)
            await self.user_repo.session.commit()
        except:
            await self.user_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"User delete error")

    async def update(self, user_id: UUID, user_data: UserUpdateDTO) -> UserDTO:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

        if user_data.username is not None:
            existing_user = await self.user_repo.get_by_username(user_data.username)
            if existing_user and existing_user.id != user.id:
                raise HTTPException(status_code=409, detail=f"Username {user_data.username} is already used by another user")

        if user_data.email is not None:
            existing_user = await self.user_repo.get_by_email(user_data.email)
            if existing_user and existing_user.id != user.id:
                raise HTTPException(status_code=409, detail=f"Email {user_data.email} is already used by another user")

        try:
            await self.user_repo.update(user, user_data)
            await self.user_repo.session.commit()
        except:
            await self.user_repo.session.rollback()
            raise HTTPException(status_code=400, detail=f"User update error")    

        return UserDTO.model_validate(user)

    async def get_user_count(self) -> int:
        return await self.user_repo.get_user_count()

    async def get_by_filter(self, count: Optional[int] = None, page: int = 1, **kwargs) -> list[UserDTO]:
        users = await self.user_repo.get_by_filter(count, page, **kwargs)
        user_dtos = [UserDTO.model_validate(user) for user in users]
        return user_dtos

    async def get_by_email(self, email: str) -> UserDTO:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise NotFoundException(detail=f"User with email {email} not found")
        return UserDTO.model_validate(user)
