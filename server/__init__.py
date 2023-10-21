from litestar import Litestar
from litestar.di import Provide

from server.auth import session_auth
from server.config import compression_config, sqlalchemy_plugin, template_config
from server.error_handlers import handle_unauthorized
from server.logging import provide_logger
from server.routing import api_router, htmx_router, mpa_router
from server.session import provide_session, session_middleware
from server.users.service import provide_user_service
from server.validation import provide_validation

app = Litestar(
    route_handlers=[api_router, mpa_router, htmx_router],
    plugins=[sqlalchemy_plugin],
    dependencies={
        "logger": Provide(provide_logger),
        "session": Provide(provide_session),
        "user_service": Provide(provide_user_service),
        "validate": Provide(provide_validation),
    },
    middleware=[session_middleware],
    on_app_init=[session_auth.on_app_init],
    template_config=template_config,
    compression_config=compression_config,
    exception_handlers={401: handle_unauthorized},  # type: ignore[assignment]
)
