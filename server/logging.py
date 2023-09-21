from picologging import Logger as _Logger
from picologging import getLogger

Logger = _Logger


async def provide_logger() -> Logger:
    return getLogger()
