import pytest

from repositories.user_repository import UserRepository
from schemas import UserAddDTO, UserDTO, UserUpdateDTO


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(
        self, user_repository: UserRepository, user_data_1: UserAddDTO
    ):
        user = await user_repository.create(user_data_1)

        assert user.id is not None
        assert user.email == user_data_1.email
        assert user.username == user_data_1.username
        assert user.description == user_data_1.description

    @pytest.mark.asyncio
    async def test_get_user_by_email(
        self, user_repository: UserRepository, user_1: UserDTO
    ):
        found_user = await user_repository.get_by_email(user_1.email)

        assert found_user.id is not None
        assert found_user.email == user_1.email
        assert found_user.username == user_1.username
        assert found_user.description == user_1.description

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository, user_1: UserDTO):
        new_user_data = UserUpdateDTO(username="Updated")

        await user_repository.update(user_1, new_user_data)

        updated_user = await user_repository.get_by_email(user_1.email)

        assert updated_user.username == new_user_data.username

        assert updated_user.id == user_1.id
        assert updated_user.email == user_1.email
        assert updated_user.description == user_1.description

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository, user_1: UserDTO):
        await user_repository.delete(user_1)

        found_user = await user_repository.get_by_email(user_1.email)
        assert found_user is None

    @pytest.mark.asyncio
    async def test_get_all_users(
        self, user_repository: UserRepository, user_1: UserDTO, user_2: UserDTO
    ):
        users_list = await user_repository.get_by_filter()

        user_emails = [user.email for user in users_list]

        assert len(users_list) == 2
        assert user_emails[0] == user_1.email
        assert user_emails[1] == user_2.email
