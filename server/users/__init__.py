from litestar.connection import ASGIConnection
from server.users.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.session import AppSession


async def retrieve_user_handler(
    session: AppSession, connection: ASGIConnection
) -> User | None:
    db_session_provider = connection.app.dependencies["db_session"]
    db_session: AsyncSession = await db_session_provider(
        state=connection.app.state, scope=connection.scope
    )
    query = select(User).where(User.id == session["user_id"])
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    return user
