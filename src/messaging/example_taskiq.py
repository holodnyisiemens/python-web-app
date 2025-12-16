from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

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
            "cron": "*/1 * * * *",
            "args": ["Cron_User"],
            "schedule_id": "greet_every_minute",
        }
    ]
)
async def my_scheduled_task(name: str) -> str:
    message = f"Scheduled hello to {name} at every minute!"
    return message
