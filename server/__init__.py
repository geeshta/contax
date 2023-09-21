from litestar import Litestar
from litestar.di import Provide

from server.auth import provide_check_owner, session_auth
from server.contacts.controllers import ContactController
from server.db import sqlalchemy_plugin
from server.logging import provide_logger
from server.session import provide_session, session_middleware
from server.users.controllers import UserController
from server.users.service import provide_user_service
from server.validation import provide_validation

app = Litestar(
    route_handlers=[UserController, ContactController],
    plugins=[sqlalchemy_plugin],
    dependencies={
        "logger": Provide(provide_logger),
        "session": Provide(provide_session),
        "user_service": Provide(provide_user_service),
        "validate": Provide(provide_validation),
        "check_owner": Provide(provide_check_owner),
    },
    middleware=[session_middleware],
    on_app_init=[session_auth.on_app_init],
)
