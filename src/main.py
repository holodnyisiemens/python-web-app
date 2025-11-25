from litestar import Litestar
from litestar.di import Provide

from controllers.user_controller import UserController
from di.providers import provide_db_session, provide_user_repository


app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
    },
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
