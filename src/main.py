from litestar import Litestar
from litestar.di import Provide
from redis.asyncio import Redis

from src.config import settings
from src.controllers.cart_controller import CartController
from src.controllers.report_controller import ReportController
from src.controllers.user_controller import UserController
from src.di.providers import (
    provide_cart_repository,
    provide_cart_service,
    provide_db_session,
    provide_redis,
    provide_report_service,
    provide_user_repository,
    provide_user_service,
)
from src.messaging.broker import broker


async def startup(app: Litestar):
    app.state.redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
    )

    await broker.connect()


async def shutdown(app: Litestar):
    await app.state.redis.aclose()
    await broker.stop()


app = Litestar(
    route_handlers=[UserController, CartController, ReportController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
        "cart_repository": Provide(provide_cart_repository),
        "cart_service": Provide(provide_cart_service),
        "report_service": Provide(provide_report_service),
        "redis": Provide(provide_redis),
    },
    on_startup=[startup],
    on_shutdown=[shutdown],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8888, reload=True)
