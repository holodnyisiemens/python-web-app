from typing import List, Annotated
from uuid import UUID

from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.params import Body
from litestar.status_codes import HTTP_200_OK

from di.providers import provide_user_service
from schemas import UserDTO, UserAddDTO, UserUpdateDTO
from services.user_service import UserService


class UserController(Controller):
    path = "/users"
    dependencies = {"user_service": Provide(provide_user_service)}

    @get("/{user_id:uuid}")
    async def get_user_by_id(self, user_service: UserService, user_id: UUID) -> UserDTO:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        return user

    @post()
    async def create_user(self, user_service: UserService, data: UserAddDTO) -> UserDTO:
        """Создать нового пользователя"""
        user = await user_service.create(data)
        return user

    @delete("/{user_id:uuid}", status_code=HTTP_200_OK)
    async def delete_user(self, user_service: UserService, user_id: UUID) -> UserDTO | None:
        """Удаление пользователя"""
        return await user_service.delete(user_id)

    @put("/{user_id:uuid}")
    async def update_user(self, user_service: UserService, user_id: UUID, data: UserUpdateDTO) -> UserDTO:
        """Обновление атрибутов пользователя"""
        return await user_service.update(user_id, data)

    @get()
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
        count: int | None = None,
        page: int = 1,
        username: str | None = None,
        email: str | None = None
    ) -> list[UserDTO]:
        """Получить пользователей с фильтрами"""
        filters = {}
        if username:
            filters["username"] = username
        if email:
            filters["email"] = email
            
        return await user_service.get_by_filter(count, page, **filters)
