from picologging import Logger, getLogger


async def logger() -> Logger:
    return getLogger()
