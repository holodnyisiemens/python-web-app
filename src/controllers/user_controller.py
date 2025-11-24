from typing import List
from uuid import UUID

from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.params import Parameter

from di.providers import provide_user_service
from schemas import UserDTO
from services.user_service import UserService


class UserController(Controller):
    path = "/users"
    dependencies = {"user_service": Provide(provide_user_service)}

    @get("/{user_id:uuid}")
    async def get_user_by_id(self, user_service: UserService, user_id: UUID) -> UserDTO:
        """Получить пользователя по ID"""
        user = await user_service.get_user_by_id(user_id)
        return user


