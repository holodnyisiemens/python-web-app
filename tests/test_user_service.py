import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from schemas import UserAddDTO, UserDTO
from repositories.user_repository import UserRepository
from services.user_service import UserService


user_data = UserAddDTO(
    username="example",
    email="email@example.com"
)


class TestUserService:
    @pytest.mark.asyncio
    async def test_create_user(self):
        # мокаем репозиторий и объекты в нем
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_user_repo.session = Mock()
        mock_user_repo.session.commit = AsyncMock()
        mock_user_repo.session.rollback = AsyncMock()

        # то, что вернёт create()
        mock_user_repo.create.return_value = {
            "id": uuid4(),
            "username": "example",
            "email": "email@example.com",
        }

        user_service = UserService(user_repo=mock_user_repo)
        result = await user_service.create(user_data)

        # проверка что для асинхронного метода create() был всего 1 await и с указанным объектом
        mock_user_repo.create.assert_awaited_once_with(user_data)
        mock_user_repo.session.commit.assert_awaited_once()
        assert isinstance(result, UserDTO)
        assert result.username == "example"

    @pytest.mark.asyncio
    async def test_delete_user(self):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_user_repo.session = Mock()
        mock_user_repo.session.commit = AsyncMock()
        mock_user_repo.session.rollback = AsyncMock()

        user_id = uuid4()

        fake_user = Mock(id=user_id, username="example", email="email@example.com")
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
