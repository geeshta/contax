import hashlib
import secrets
import base64
import logging
from litestar.exceptions import InternalServerException


class UserSecurityService:
    @staticmethod
    def hash_password(password: str, iterations: int = 1000) -> str:
        """Generate a secure hash from the password.
        Number of iterations must be greater than 0.
        """
        if not iterations > 0:
            raise ValueError("Number of iterations must be greater than 0")

        try:
            salt = secrets.token_bytes(16)

            hashed_password = hashlib.pbkdf2_hmac(
                "sha256", password.encode(), salt, iterations
            )

            b64_hash = base64.b64encode(hashed_password).decode("ascii")
            b64_salt = base64.b64encode(salt).decode("ascii")

        except Exception as err:
            logging.error(f"An error occured while hashing the password: {err}")
            raise InternalServerException(
                "An error occured. Check server logs for more information",
                status_code=500,
            )

        else:
            logging.info(f"{b64_hash}")

            return f"sha256:{iterations}:{b64_salt}:{b64_hash}"


def user_security_service() -> UserSecurityService:
    return UserSecurityService()
