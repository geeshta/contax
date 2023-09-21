from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware.session.client_side import ClientSideSessionBackend
from litestar.security.session_auth import SessionAuth
from litestar.status_codes import HTTP_401_UNAUTHORIZED
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from server.logging import Logger
from server.session import AppSession, SessionProxy, session_config
from server.users.models import User
from server.users.service import UserService


async def retrieve_user_handler(
    session: AppSession, connection: ASGIConnection
) -> User | None:
    db_session_provider = connection.app.dependencies["db_session"]
    logger_provider = connection.app.dependencies["logger"]
    transaction_provider = connection.app.dependencies["transaction"]
    user_service_provider = connection.app.dependencies["user_service"]

    db_session: AsyncSession = await db_session_provider(
        state=connection.app.state, scope=connection.scope
    )
    logger: Logger = await logger_provider()
    transaction_generator: AsyncGenerator[
        AsyncSession, None
    ] = await transaction_provider(db_session=db_session)

    transaction = await anext(transaction_generator)

    try:
        user_service: UserService = await user_service_provider(
            logger=logger, db_session=db_session, transaction=transaction_generator
        )
        if "user_id" not in session:
            return None

        user = await user_service.get_by_id(session["user_id"], raise_404=False)
        return user

    finally:
        await transaction.aclose()


session_auth = SessionAuth[User, ClientSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=session_config,
    exclude="/schema",
)


async def provide_current_user_id(session: SessionProxy) -> int:
    if not "user_id" in session:
        raise NotAuthorizedException(
            "Please log in to access this resource",
            status_code=HTTP_401_UNAUTHORIZED,
        )
    return session["user_id"]
