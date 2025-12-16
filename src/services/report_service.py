from datetime import datetime
from typing import Optional

from litestar.exceptions import HTTPException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.repositories.report_repository import ReportRepository
from src.schemas import ReportAddDTO, ReportDTO


class ReportService:
    def __init__(self, report_repo: ReportRepository):
        self.report_repo = report_repo

    async def get_by_cart_id(self, cart_id: int) -> ReportDTO:
        report = await self.report_repo.get_by_cart_id(cart_id)

        if not report:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Report with cart_id {cart_id} not found",
            )

        return ReportDTO.model_validate(report)

    async def create(self, report_data: ReportAddDTO) -> ReportDTO:
        try:
            report = await self.report_repo.create(report_data)
            await self.report_repo.session.commit()
        except Exception as exc:
            await self.report_repo.session.rollback()
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Report create error"
            ) from exc

        return ReportDTO.model_validate(report)

    async def get_by_date(
        self,
        date_from: Optional[datetime] = None,
        date_before: Optional[datetime] = None,
    ) -> list[ReportDTO]:
        reports = await self.report_repo.get_by_date(date_from, date_before)
        return [ReportDTO.model_validate(report) for report in reports]
