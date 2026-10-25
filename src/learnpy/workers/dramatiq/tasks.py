"""Dramatiq worker 示例。"""

from __future__ import annotations

import os
from typing import Final

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

DEFAULT_REDIS_URL: Final[str] = "redis://localhost:6379/0"
REDIS_URL: Final[str] = os.getenv("TASK_QUEUE_REDIS_URL", DEFAULT_REDIS_URL)

result_backend = RedisBackend(url=REDIS_URL)
redis_broker = RedisBroker(url=REDIS_URL)
redis_broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(redis_broker)


@dramatiq.actor(max_retries=3, min_backoff=1_000, store_results=True)
def add(x: int, y: int) -> int:
    """求和。"""
    return x + y


@dramatiq.actor(max_retries=3, min_backoff=1_000, store_results=True)
def multiply(x: int, y: int) -> int:
    """求积。"""
    return x * y
