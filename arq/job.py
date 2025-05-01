import asyncio

from arq import create_pool
from arq.connections import RedisSettings


async def main():
    redis = await create_pool(RedisSettings(host="43.156.74.18", port=6379, database=0))
    job = await redis.enqueue_job("add", 3, 7)
    result = await job.result(timeout=5)  # 等待任务完成并获取结果
    print(f"Got result: {result}")


asyncio.run(main())
