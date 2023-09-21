from server.session import session_config
from server.users import retrieve_user_handler
from litestar.security.session_auth import SessionAuth
from litestar.middleware.session.client_side import ClientSideSessionBackend
from server.users.models import User

session_auth = SessionAuth[User, ClientSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=session_config,
    exclude="/schema",
)
