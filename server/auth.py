from litestar.connection import ASGIConnection
from litestar.middleware.session.client_side import ClientSideSessionBackend
from litestar.security.session_auth import SessionAuth
from sqlalchemy.ext.asyncio import AsyncSession

from server.logging import Logger
from server.session import AppSession, session_config
from server.users.models import User
from server.users.service import UserService


async def retrieve_user_handler(
    session: AppSession, connection: ASGIConnection
) -> User | None:
    db_session_provider = connection.app.dependencies["db_session"]
    logger_provider = connection.app.dependencies["logger"]
    user_service_provider = connection.app.dependencies["user_service"]

    db_session: AsyncSession = await db_session_provider(
        state=connection.app.state, scope=connection.scope
    )
    logger: Logger = await logger_provider()
    user_service: UserService = await user_service_provider(
        logger=logger, db_session=db_session
    )
    if "user_id" not in session:
        return None

    user = await user_service.get_by_id(session["user_id"], raise_404=False)
    return user


session_auth = SessionAuth[User, ClientSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=session_config,
    exclude="/schema",
)
