import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.config import settings

broker = RabbitBroker(settings.rabbit_url)
app = FastStream(broker)


@broker.subscriber("order")
async def handle(msg):
    print(msg)


@app.after_startup
async def test_publish():
    await broker.publish(
        message="test_message",
        queue="order",
    )


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
