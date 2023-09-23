from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware.session.client_side import ClientSideSessionBackend
from litestar.security.session_auth import SessionAuth
from litestar.status_codes import HTTP_401_UNAUTHORIZED
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.session import AppSession, session_config
from server.users.models import User


async def retrieve_user_handler(
    session: AppSession, connection: ASGIConnection
) -> User | None:
    db_session_provider = connection.app.dependencies["db_session"]

    db_session: AsyncSession = await db_session_provider(
        state=connection.app.state, scope=connection.scope
    )

    user_id = session.get("user_id", None)
    if user_id:
        query = select(User).where(User.id == user_id)
        result = await db_session.execute(query)
        user = result.scalar_one_or_none()
        return user

    return None


session_auth = SessionAuth[User, ClientSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=session_config,
    exclude="/schema",
)
