from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

from src.database import async_session_factory
from src.repositories.report_repository import ReportRepository
from src.schemas import ReportAddDTO
from src.services.report_service import ReportService

broker = AioPikaBroker(
    "amqp://guest:guest@localhost:5672/local",
    exchange_name="report",  # обменник
    queue_name="cmd_cart",  # очередь для отправки
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(
    schedule=[
        {
            "cron": "*/5 * * * *",
            "args": ["Cron_User"],
            "schedule_id": "report_every_minute",
        }
    ]
)
async def report_scheduler():
    report_data = ReportAddDTO(
        order_id=1,
        count_product=5,
    )

    async with async_session_factory() as session:
        report_repo = ReportRepository(session)
        report_service = ReportService(report_repo)

        report_service.create(report_data)

    message = f"Scheduled report"
    return message
