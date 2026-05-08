"""Dramatiq worker 示例。

启动命令:
    dramatiq work
"""

from __future__ import annotations

import os
from typing import Final

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

DEFAULT_REDIS_URL: Final[str] = "redis://43.156.74.18:6379/0"
REDIS_URL: Final[str] = os.getenv("TASK_QUEUE_REDIS_URL", DEFAULT_REDIS_URL)

result_backend = RedisBackend(url=REDIS_URL)
redis_broker = RedisBroker(url=REDIS_URL)
redis_broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(redis_broker)


@dramatiq.actor(max_retries=3, min_backoff=1_000, store_results=True)
def add(x: int, y: int) -> int:
    """计算两个整数的和。

    Args:
        x: 第一个整数。
        y: 第二个整数。

    Returns:
        两个整数相加后的结果。
    """
    return x + y


@dramatiq.actor(max_retries=3, min_backoff=1_000, store_results=True)
def multiply(x: int, y: int) -> int:
    """计算两个整数的乘积。

    Args:
        x: 第一个整数。
        y: 第二个整数。

    Returns:
        两个整数相乘后的结果。
    """
    return x * y
