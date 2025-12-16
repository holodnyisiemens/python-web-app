import pytest

from src.schemas import UserAddDTO, UserDTO


class TestUserController:
    @pytest.mark.asyncio
    async def test_get_user_by_id(
        self, mock_user_service, client, user_data_1: UserAddDTO
    ):
        user_id = 1
        expected_user = UserDTO(
            id=user_id,
            username=user_data_1.username,
            email=user_data_1.email,
        )

        mock_user_service.get_by_id.return_value = expected_user

        response = await client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == user_id
        assert data["username"] == user_data_1.username
        assert data["email"] == user_data_1.email

        mock_user_service.get_by_id.assert_awaited_once_with(user_id)
