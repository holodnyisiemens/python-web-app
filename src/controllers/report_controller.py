from datetime import datetime
from typing import Optional

from litestar import Controller, get

from src.schemas import ReportDTO
from src.services.report_service import ReportService


class ReportController(Controller):
    path = "/reports"

    @get("/{cart_id:int}")
    async def get_report_by_cart_id(
        self, report_service: ReportService, cart_id: int
    ) -> ReportDTO:
        """Получить отчет по ID заказа"""
        return await report_service.get_by_cart_id(cart_id)

    @get("/")
    async def get_reports_by_date(
        self,
        report_service: ReportService,
        date_from: Optional[datetime] = None,
        date_before: Optional[datetime] = None,
    ) -> list[ReportDTO]:
        """Получить отчеты по дате"""
        reports = await repowrt_service.get_by_date(date_from, date_before)
        return reports
