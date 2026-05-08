"""Celery worker 示例。

启动命令:
    celery -A work worker --loglevel=info
"""

from __future__ import annotations

import os
from typing import Final

from celery import Celery

DEFAULT_REDIS_URL: Final[str] = "redis://43.156.74.18:6379/0"
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
    """计算两个整数的和。

    Args:
        x: 第一个整数。
        y: 第二个整数。

    Returns:
        两个整数相加后的结果。
    """
    return x + y


@app.task(name="celery.multiply")
def multiply(x: int, y: int) -> int:
    """计算两个整数的乘积。

    Args:
        x: 第一个整数。
        y: 第二个整数。

    Returns:
        两个整数相乘后的结果。
    """
    return x * y


@app.task(name="celery.sum_numbers")
def sum_numbers(numbers: list[int]) -> int:
    """汇总整数列表。

    Args:
        numbers: 需要求和的整数列表。

    Returns:
        列表元素的总和。
    """
    return sum(numbers)
