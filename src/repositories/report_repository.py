from datetime import datetime
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Report
from src.schemas import ReportAddDTO


class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_cart_id(self, cart_id: int) -> Optional[Report]:
        return await self.session.get(Report, cart_id)

    async def create(self, report_data: ReportAddDTO) -> Report:
        report = Report(**report_data.model_dump())
        self.session.add(report)

        await self.session.flush()
        await self.session.refresh(report)

        return report

    async def get_all(self) -> list[Report]:
        stmt = select(Report)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_date(
        self,
        date_from: Optional[datetime] = None,
        date_before: Optional[datetime] = None,
    ) -> Optional[Report]:
        stmt = select(Report)

        conditions = []

        if date_from:
            conditions.append(Report.report_at >= date_from)

        if date_before:
            conditions.append(Report.report_at < date_before)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        # сортируем по дате отчета (новые сверху)
        stmt = stmt.order_by(Report.report_at.desc())

        result = await self.session.execute(stmt)

        return result.unique().scalars().all()
