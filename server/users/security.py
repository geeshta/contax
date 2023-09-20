import hashlib
import secrets
import base64
import logging
from litestar.exceptions import InternalServerException
from typing import TypedDict


class HashInfo(TypedDict):
    hash: bytes
    salt: bytes
    iterations: int


class UserSecurityService:
    @staticmethod
    def _generate_hash(
        password: str, iterations: int, salt: bytes | None = None
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
            logging.error(f"An error occured while hashing the password: {err}")
            raise InternalServerException(
                "An error occured. Check server logs for more information.",
                status_code=500,
            ) from err

    @staticmethod
    def _parse_hash(hash_string: str) -> HashInfo:
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
            logging.error(f"An error occured while parsing the hash: {err}")
            raise InternalServerException(
                "An error occured. Check server logs for more information.",
                status_code=500,
            ) from err

    @staticmethod
    def hash_password(password: str, iterations: int = 1000) -> str:
        """Generate a secure hash from the password.
        Number of iterations must be greater than 0.
        """
        hash_info = UserSecurityService._generate_hash(password, iterations)
        b64_hash = base64.b64encode(hash_info["hash"]).decode("ascii")
        b64_salt = base64.b64encode(hash_info["salt"]).decode("ascii")
        hash_string = f"sha256:{iterations}:{b64_salt}:{b64_hash}"
        logging.info(hash_string)
        return hash_string

    @staticmethod
    def verify_password(password: str, hash_string: str) -> bool:
        """
        Verify if a given password matches a given encoded hash string
        """
        info_from_hash = UserSecurityService._parse_hash(hash_string)
        info_from_password = UserSecurityService._generate_hash(
            password=password,
            iterations=info_from_hash["iterations"],
            salt=info_from_hash["salt"],
        )

        return info_from_hash["hash"] == info_from_password["hash"]


async def user_security_service() -> UserSecurityService:
    return UserSecurityService()
