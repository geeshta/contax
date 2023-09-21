from litestar.connection import ASGIConnection
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.session import AppSession
from server.users.models import User


async def retrieve_user_handler(
    session: AppSession, connection: ASGIConnection
) -> User | None:
    db_session_provider = connection.app.dependencies["db_session"]
    db_session: AsyncSession = await db_session_provider(
        state=connection.app.state, scope=connection.scope
    )

    user_id = session.get("user_id")
    if user_id is None:
        return None

    query = select(User).where(User.id == user_id)
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()

    return user
