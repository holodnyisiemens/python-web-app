from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Address
from src.schemas import AddressAddDTO, AddressUpdateDTO


class AddressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, address_id: int) -> Optional[Address]:
        return await self.session.get(Address, address_id)

    async def create(self, address_data: AddressAddDTO) -> Address:
        address = Address(**address_data.model_dump())
        self.session.add(address)

        await self.session.flush()
        await self.session.refresh(address)

        return address

    async def delete(self, address_id: int) -> Optional[Address]:
        stmt = select(Address).where(Address.id == address_id)
        result = await self.session.execute(stmt)
        address = result.scalar_one_or_none()
        if not address:
            return None
        await self.session.delete(address)
        await self.session.commit()
        return address

    async def update(self, address_id: int, address_data: AddressUpdateDTO) -> Address:
        stmt = select(Address).where(Address.id == address_id)
        result = await self.session.execute(stmt)
        address = result.scalar_one_or_none()
        if not address:
            return None
        # обновляем только переданные поля
        update_data = address_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(address, field, value)

        await self.session.commit()
        await self.session.refresh(address)
        return address
