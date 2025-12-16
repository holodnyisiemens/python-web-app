import json
from unittest.mock import AsyncMock, Mock

import pytest
from redis.asyncio import Redis

from src.repositories.user_repository import UserRepository
from src.schemas import UserAddDTO, UserDTO
from src.services.user_service import UserService


class TestUserService:
    @pytest.mark.asyncio
    async def test_create_user(self, user_data_1: UserAddDTO, redis: Redis):
        # мокаем репозиторий и объекты в нем
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_user_repo.session = Mock()
        mock_user_repo.session.commit = AsyncMock()
        mock_user_repo.session.rollback = AsyncMock()

        # то, что вернёт create()
        mock_user_repo.create.return_value = UserDTO(
            id=1, username=user_data_1.username, email=user_data_1.email
        )

        user_service = UserService(user_repo=mock_user_repo, redis=redis)
        result = await user_service.create(user_data_1)

        # проверка что для асинхронного метода create() был всего 1 await и с указанным объектом
        mock_user_repo.create.assert_awaited_once_with(user_data_1)
        mock_user_repo.session.commit.assert_awaited_once()
        assert isinstance(result, UserDTO)
        assert result.username == user_data_1.username

    @pytest.mark.asyncio
    async def test_delete_user(self, user_data_1: UserAddDTO, redis: Redis):
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

        user_service = UserService(user_repo=mock_user_repo, redis=redis)
        result = await user_service.delete(user_id)

        assert result is None

        mock_user_repo.get_by_id.assert_awaited_once_with(user_id)
        mock_user_repo.delete.assert_awaited_once_with(fake_user)
        mock_user_repo.session.commit.assert_awaited_once()

        # rollback не должен быть вызван
        mock_user_repo.session.rollback.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_id_cache_hit(self, redis: Redis):
        # подготовка: данные уже есть в кэше
        user_id = 1
        cached_user = {"id": user_id, "username": "test", "email": "test@example.com"}
        await redis.set(f"user:{user_id}", json.dumps(cached_user))

        mock_user_repo = AsyncMock()
        user_service = UserService(user_repo=mock_user_repo, redis=redis)

        result = await user_service.get_by_id(user_id)

        # данные вернулись из кэша
        assert result.id == user_id
        assert result.username == "test"

        # метод репозитория не вызывался
        mock_user_repo.get_by_id.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_by_id_cache_miss(self, redis: Redis):
        # подготовка: кэша нет
        user_id = 2
        mock_user_repo = AsyncMock()
        fake_user = {"id": user_id, "username": "test", "email": "test@example.com"}
        mock_user_repo.get_by_id.return_value = fake_user

        user_service = UserService(user_repo=mock_user_repo, redis=redis)

        result = await user_service.get_by_id(user_id)

        assert result.id == user_id
        assert result.username == "test"

        # метод репозитория был вызван
        mock_user_repo.get_by_id.assert_awaited_once_with(user_id)

        # данные должны оказаться в кэше
        cached = await redis.get(f"user:{user_id}")
        assert cached is not None
        cached_data = json.loads(cached)
        assert cached_data["username"] == "test"
