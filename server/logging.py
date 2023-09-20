from picologging import getLogger, Logger


async def logger() -> Logger:
    return getLogger()
