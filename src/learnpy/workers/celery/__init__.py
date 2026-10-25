"""Celery 任务队列示例。"""

from learnpy.workers.celery.tasks import (
    REDIS_URL,
    add,
    app,
    multiply,
    sum_numbers,
)

__all__ = ["REDIS_URL", "add", "app", "multiply", "sum_numbers"]
