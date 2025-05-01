# worker.py
from arq import func
from arq.connections import RedisSettings


async def add(ctx, a, b):
    return a + b


class WorkerSettings:
    functions = [add]
    redis_settings = RedisSettings(host="43.156.74.18", port=6379, database=0)
