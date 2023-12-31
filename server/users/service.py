import base64
import hashlib
import secrets
from typing import TypedDict, TypeVar, overload

from litestar.exceptions import (
    ClientException,
    InternalServerException,
    NotAuthorizedException,
    NotFoundException,
)
from litestar.status_codes import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.logging import Logger
from server.service import AbstractService
from server.users.models import User

T = TypeVar("T")


class HashInfo(TypedDict):
    hash: bytes
    salt: bytes
    iterations: int


class UserService(AbstractService):
    def _generate_hash(
        self, password: str, iterations: int, salt: bytes | None = None
    ) -> HashInfo:
        """
        Hash a given string and generate information about the hash in a dict
        """
        if not iterations > 0:
            raise ValueError("Number of iterations must be greater than 0")
        try:
            if salt is None:
                salt = secrets.token_bytes(16)

            hashed_password = hashlib.pbkdf2_hmac(
                "sha256", password.encode(), salt, iterations
            )

            return {"hash": hashed_password, "salt": salt, "iterations": iterations}

        except Exception as err:
            self.logger.error(f"An error occured while hashing the password: {err}")
            raise InternalServerException(
                "An error occured. Check server logs for more information.",
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            ) from err

    def _parse_hash(self, hash_string: str) -> HashInfo:
        """
        Parse a given hash and return the encoded information as a dict
        """
        try:
            match hash_string.split(":"):
                case ["sha256", iterations, salt, hash]:
                    iterations = int(iterations)
                    salt = base64.b64decode(salt.encode("ascii"))
                    hash = base64.b64decode(hash.encode("ascii"))
                    return {"hash": hash, "salt": salt, "iterations": iterations}
                case _:
                    raise ValueError(
                        f"Hash string is not in the correct format: {hash_string}"
                    )
        except Exception as err:
            self.logger.error(f"An error occured while parsing the hash: {err}")
            raise InternalServerException(
                "An error occured. Check server logs for more information.",
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            ) from err

    def hash_password(self, password: str, iterations: int = 1000) -> str:
        """Generate a secure hash from the password.
        Number of iterations must be greater than 0.
        """
        hash_info = self._generate_hash(password, iterations)
        b64_hash = base64.b64encode(hash_info["hash"]).decode("ascii")
        b64_salt = base64.b64encode(hash_info["salt"]).decode("ascii")
        hash_string = f"sha256:{iterations}:{b64_salt}:{b64_hash}"
        return hash_string

    def verify_password(self, password: str, hash_string: str) -> bool:
        """
        Verify if a given password matches a given encoded hash string
        """
        info_from_hash = self._parse_hash(hash_string)
        info_from_password = self._generate_hash(
            password=password,
            iterations=info_from_hash["iterations"],
            salt=info_from_hash["salt"],
        )

        return info_from_hash["hash"] == info_from_password["hash"]

    @overload
    async def get_by_id(self, id: int) -> User:
        ...

    @overload
    async def get_by_id(self, id: int, raise_404: bool) -> User | None:
        ...

    async def get_by_id(self, id: int, raise_404: bool = True) -> User | None:
        query = select(User).where(User.id == id)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()

        if user is None and raise_404:
            self.logger.error(f"User with id {id} not found.")
            raise NotFoundException("User not found.", status_code=HTTP_404_NOT_FOUND)
        return user

    async def create_user(self, email: str, password: str) -> User:
        hash_string = self.hash_password(password)
        user = User(email=email, password_hash=hash_string)
        try:
            self.db_session.add(user)
            await self.db_session.flush()
        except IntegrityError:
            raise ClientException(
                detail=f"User with email {email} already exists.",
                status_code=HTTP_409_CONFLICT,
            )
        return user

    @overload
    async def authenticate_user(self, email: str, password: str) -> User:
        ...

    @overload
    async def authenticate_user(
        self, email: str, password: str, raise_401: bool
    ) -> User | None:
        ...

    async def authenticate_user(
        self, email: str, password: str, raise_401: bool = True
    ) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            if raise_401:
                raise NotAuthorizedException(
                    "Invalid credentials", status_code=HTTP_401_UNAUTHORIZED
                )
            else:
                return None

        is_authenticated = self.verify_password(password, user.password_hash)

        if not is_authenticated:
            if raise_401:
                raise NotAuthorizedException(
                    "Invalid credentials", status_code=HTTP_401_UNAUTHORIZED
                )
            else:
                return None

        return user


async def provide_user_service(logger: Logger, db_session: AsyncSession) -> UserService:
    return UserService(db_session, logger)
