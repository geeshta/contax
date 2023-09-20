import hashlib
import secrets
import base64
from litestar.exceptions import InternalServerException
from typing import TypedDict
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from picologging import Logger


class HashInfo(TypedDict):
    hash: bytes
    salt: bytes
    iterations: int


class UserSecurityService:
    def __init__(self, logger: Logger):
        self.logger = logger

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


async def user_security_service(logger: Logger) -> UserSecurityService:
    return UserSecurityService(logger)
