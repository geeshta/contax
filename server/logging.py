from picologging import Logger as _Logger, getLogger

Logger = _Logger


async def provide_logger() -> Logger:
    return getLogger()
