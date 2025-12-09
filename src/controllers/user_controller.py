from typing import Optional

from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.status_codes import HTTP_200_OK

from di.providers import provide_user_service
from schemas import UserDTO, UserAddDTO, UserUpdateDTO
from services.user_service import UserService


class UserController(Controller):
    path = "/users"
    
    @get("/{user_id:int}", status_code=HTTP_200_OK)
    async def get_user_by_id(self, user_service: UserService, user_id: int) -> UserDTO:
        """Получить пользователя по ID""" 
        return await user_service.get_by_id(user_id)

    @post()
    async def create_user(self, user_service: UserService, data: UserAddDTO) -> UserDTO:
        """Создать нового пользователя"""
        return await user_service.create(data)

    @delete("/{user_id:int}", status_code=HTTP_200_OK)
    async def delete_user(self, user_service: UserService, user_id: int) -> UserDTO | None:
        """Удаление пользователя"""
        return await user_service.delete(user_id)

    @put("/{user_id:int}")
    async def update_user(self, user_service: UserService, user_id: int, data: UserUpdateDTO) -> UserDTO:
        """Обновление атрибутов пользователя"""
        return await user_service.update(user_id, data)

    @get("/", status_code=HTTP_200_OK)
    async def get_all_users(self, user_service: UserService) -> dict:
        """Получить всех пользователей"""
        users = await user_service.get_by_filter()
        total_count = await user_service.get_user_count()
        return {
            "users": users,
            "total_count": total_count
        }

    @get("/filter")
    async def get_users_with_filters(
        self, 
        user_service: UserService,
        count: Optional[int] = None,
        page: int = 1,
        username: Optional[str] = None,
        email: Optional[str] = None
    ) -> list[UserDTO]:
        """Получить пользователей с фильтрами"""
        filters = {}
        if username:
            filters["username"] = username
        if email:
            filters["email"] = email
            
        return await user_service.get_by_filter(count, page, **filters)
