"""Celery worker 示例。"""

from __future__ import annotations

import os
from typing import Final

from celery import Celery

DEFAULT_REDIS_URL: Final[str] = "redis://localhost:6379/0"
REDIS_URL: Final[str] = os.getenv("TASK_QUEUE_REDIS_URL", DEFAULT_REDIS_URL)

app = Celery("task_queue_examples", broker=REDIS_URL, backend=REDIS_URL)
app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    enable_utc=False,
    task_track_started=True,
    task_time_limit=30,
    result_expires=3600,
)


@app.task(name="celery.add")
def add(x: int, y: int) -> int:
    """求和。"""
    return x + y


@app.task(name="celery.multiply")
def multiply(x: int, y: int) -> int:
    """求积。"""
    return x * y


@app.task(name="celery.sum_numbers")
def sum_numbers(numbers: list[int]) -> int:
    """求列表总和。"""
    return sum(numbers)
