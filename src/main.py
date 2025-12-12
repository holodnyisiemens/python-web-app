from litestar import Litestar
from litestar.di import Provide

from controllers.cart_controller import CartController
from controllers.user_controller import UserController
from di.providers import (
    provide_cart_repository,
    provide_cart_service,
    provide_db_session,
    provide_user_repository,
    provide_user_service,
)

app = Litestar(
    route_handlers=[UserController, CartController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
        "cart_repository": Provide(provide_cart_repository),
        "cart_service": Provide(provide_cart_service),
    },
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
