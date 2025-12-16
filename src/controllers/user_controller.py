from typing import Optional

from litestar import Controller, delete, get, post, put

from src.schemas import UserAddDTO, UserDTO, UserUpdateDTO
from src.services.user_service import UserService


class UserController(Controller):
    path = "/users"

    @get("/{user_id:int}")
    async def get_user_by_id(self, user_service: UserService, user_id: int) -> UserDTO:
        """Получить пользователя по ID"""
        return await user_service.get_by_id(user_id)

    @post()
    async def create_user(self, user_service: UserService, data: UserAddDTO) -> UserDTO:
        """Создать нового пользователя"""
        return await user_service.create(data)

    @delete("/{user_id:int}")
    async def delete_user(self, user_service: UserService, user_id: int) -> None:
        """Удаление пользователя"""
        return await user_service.delete(user_id)

    @put("/{user_id:int}")
    async def update_user(
        self, user_service: UserService, user_id: int, data: UserUpdateDTO
    ) -> UserDTO:
        """Обновление атрибутов пользователя"""
        return await user_service.update(user_id, data)

    @get("/")
    async def get_all_users(self, user_service: UserService) -> dict:
        """Получить всех пользователей"""
        users = await user_service.get_by_filter()
        total_count = await user_service.get_user_count()
        return {"users": users, "total_count": total_count}

    @get("/filter")
    async def get_users_with_filters(
        self,
        user_service: UserService,
        count: Optional[int] = None,
        page: int = 1,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> list[UserDTO]:
        """Получить пользователей с фильтрами"""
        filters = {}
        if username:
            filters["username"] = username
        if email:
            filters["email"] = email

        return await user_service.get_by_filter(count, page, **filters)
