from litestar import Litestar
from litestar.di import Provide

from server.auth import session_auth
from server.db import provide_transaction, sqlalchemy_plugin
from server.logging import provide_logger
from server.routers import api_router, mpa_router
from server.session import provide_session, session_middleware
from server.templating import template_config
from server.users.service import provide_user_service
from server.validation import provide_validation

app = Litestar(
    route_handlers=[api_router, mpa_router],
    plugins=[sqlalchemy_plugin],
    dependencies={
        "transaction": Provide(provide_transaction),
        "logger": Provide(provide_logger),
        "session": Provide(provide_session),
        "user_service": Provide(provide_user_service),
        "validate": Provide(provide_validation),
    },
    middleware=[session_middleware],
    on_app_init=[session_auth.on_app_init],
    template_config=template_config,
)
