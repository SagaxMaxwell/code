"""ARQ producer 示例。"""

from __future__ import annotations

import asyncio

from arq import create_pool

from python_notes.task_queues.arq.tasks import redis_config_from_env


async def submit_single_task() -> None:
    """提交一个普通异步任务并等待结果。"""
    redis = await create_pool(redis_config_from_env().to_settings())
    try:
        job = await redis.enqueue_job("add", 3, 7, _queue_name="arq:queue")
        result = await job.result(timeout=5)
        print("Job ID:", job.job_id)
        print("Result:", result)
    finally:
        await redis.close()


async def submit_delayed_and_retry_tasks() -> None:
    """提交延迟任务和带重试逻辑的任务。"""
    redis = await create_pool(redis_config_from_env().to_settings())
    try:
        delayed = await redis.enqueue_job("multiply", 6, 7, _defer_by=2)
        retried = await redis.enqueue_job("flaky_job", 21)
        print("Delayed Job ID:", delayed.job_id)
        print("Retry Result:", await retried.result(timeout=10))
    finally:
        await redis.close()


async def main() -> None:
    """运行 producer 示例。"""
    await submit_single_task()
    await submit_delayed_and_retry_tasks()


if __name__ == "__main__":
    asyncio.run(main())
