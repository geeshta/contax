from picologging import Logger, getLogger


async def provide_logger() -> Logger:
    return getLogger()
