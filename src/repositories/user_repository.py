from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas import UserAddDTO, UserUpdateDTO


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user_data: UserAddDTO) -> User:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None
        await self.session.delete(user)
        await self.session.commit()
        return user

    async def update(self, user_id: UUID, user_data: UserUpdateDTO) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None
        # обновляем только переданные поля
        update_data = user_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user_count(self) -> int:
        result = await self.session.execute(select(func.count(User.id)))
        return result.scalar_one()
    
    async def get_by_filter(self, count: Optional[int] = None, page: int = 1, **kwargs) -> list[User]:
        stmt = select(User)
        
        # фильтры
        for field, value in kwargs.items():
            if hasattr(User, field) and value is not None:
                stmt = stmt.where(getattr(User, field) == value)
        
        # пагинация если указан count
        if count:
            stmt = stmt.offset((page - 1) * count).limit(count)

        users = (await self.session.execute(stmt)).scalars().all()
        return users
