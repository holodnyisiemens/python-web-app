import pytest

from schemas import UserAddDTO
from repositories.user_repository import UserRepository


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        user_data = UserAddDTO(
            username="john_doe",
            email="test@example.com",
            description="test user",
        )

        user = await user_repository.create(user_data)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "john_doe"
        assert user.description == "test user"
