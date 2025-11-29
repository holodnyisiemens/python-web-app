import pytest

from schemas import UserAddDTO, UserUpdateDTO
from repositories.user_repository import UserRepository


class TestUserRepository:
    async def _create_test_user(self, user_repository: UserRepository):
        user_data = UserAddDTO(
            username="john_doe",
            email="test@example.com",
            description="test user",
        )
        user = await user_repository.create(user_data)
        return user, user_data    

    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        user, user_data = await self._create_test_user(user_repository)

        assert user.id is not None
        assert user.email == user_data.email
        assert user.username == user_data.username
        assert user.description == user_data.description

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, user_repository: UserRepository):
        _, user_data = await self._create_test_user(user_repository)

        found_user = await user_repository.get_by_email(user_data.email)

        assert found_user.id is not None
        assert found_user.email == user_data.email
        assert found_user.username == user_data.username
        assert found_user.description == user_data.description

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository):
        user, user_data = await self._create_test_user(user_repository)

        new_user_data = UserUpdateDTO(username="Updated")

        await user_repository.update(user.id, new_user_data)

        updated_user = await user_repository.get_by_email(user_data.email)
        
        assert updated_user.username == new_user_data.username

        assert updated_user.id == user.id
        assert updated_user.email == user.email
        assert updated_user.description == user.description

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository):
        user, user_data = await self._create_test_user(user_repository)

        await user_repository.delete(user.id)

        found_user = await user_repository.get_by_email(user_data.email)

        assert found_user is None
