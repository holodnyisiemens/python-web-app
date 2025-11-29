import pytest

from schemas import UserAddDTO, UserUpdateDTO, UserDTO
from repositories.user_repository import UserRepository


user_data_1 = UserAddDTO(
    username="john_doe",
    email="john@example.com",
    description="test user 1",
)

user_data_2 = UserAddDTO(
    username="jason_smith",
    email="jason@example.com",
    description="test user 2",
)


class TestUserRepository:
    async def _create_test_user(self, user_repository: UserRepository, user_data: UserAddDTO) -> UserDTO:
        user = await user_repository.create(user_data)
        return user

    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        user = await self._create_test_user(user_repository, user_data_1)

        assert user.id is not None
        assert user.email == user_data_1.email
        assert user.username == user_data_1.username
        assert user.description == user_data_1.description

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, user_repository: UserRepository):
        await self._create_test_user(user_repository, user_data_1)

        found_user = await user_repository.get_by_email(user_data_1.email)

        assert found_user.id is not None
        assert found_user.email == user_data_1.email
        assert found_user.username == user_data_1.username
        assert found_user.description == user_data_1.description

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository):
        user = await self._create_test_user(user_repository, user_data_1)

        new_user_data = UserUpdateDTO(username="Updated")

        await user_repository.update(user.id, new_user_data)

        updated_user = await user_repository.get_by_email(user_data_1.email)
        
        assert updated_user.username == new_user_data.username

        assert updated_user.id == user.id
        assert updated_user.email == user.email
        assert updated_user.description == user.description

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository):
        user = await self._create_test_user(user_repository, user_data_1)
        await user_repository.delete(user.id)

        found_user = await user_repository.get_by_email(user_data_1.email)
        assert found_user is None
