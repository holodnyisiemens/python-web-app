from unittest.mock import AsyncMock, Mock

import pytest

from repositories.user_repository import UserRepository
from schemas import UserAddDTO, UserDTO
from services.user_service import UserService


class TestUserService:
    @pytest.mark.asyncio
    async def test_create_user(self, user_data_1: UserAddDTO):
        # мокаем репозиторий и объекты в нем
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_user_repo.session = Mock()
        mock_user_repo.session.commit = AsyncMock()
        mock_user_repo.session.rollback = AsyncMock()

        # то, что вернёт create()
        mock_user_repo.create.return_value = UserDTO(
            id=1, username=user_data_1.username, email=user_data_1.email
        )

        user_service = UserService(user_repo=mock_user_repo)
        result = await user_service.create(user_data_1)

        # проверка что для асинхронного метода create() был всего 1 await и с указанным объектом
        mock_user_repo.create.assert_awaited_once_with(user_data_1)
        mock_user_repo.session.commit.assert_awaited_once()
        assert isinstance(result, UserDTO)
        assert result.username == user_data_1.username

    @pytest.mark.asyncio
    async def test_delete_user(self, user_data_1: UserAddDTO):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_user_repo.session = Mock()
        mock_user_repo.session.commit = AsyncMock()
        mock_user_repo.session.rollback = AsyncMock()

        user_id = 1
        fake_user = Mock(
            id=user_id,
            username=user_data_1.username,
            email=user_data_1.email,
        )

        mock_user_repo.get_by_id.return_value = fake_user

        mock_user_repo.delete.return_value = None

        user_service = UserService(user_repo=mock_user_repo)
        result = await user_service.delete(user_id)

        assert result is None

        mock_user_repo.get_by_id.assert_awaited_once_with(user_id)
        mock_user_repo.delete.assert_awaited_once_with(fake_user)
        mock_user_repo.session.commit.assert_awaited_once()

        # rollback не должен быть вызван
        mock_user_repo.session.rollback.assert_not_called()
