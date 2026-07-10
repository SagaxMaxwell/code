"""Celery 任务队列示例。"""

from python_notes.examples.task_queues.celery.tasks import (
    REDIS_URL,
    add,
    app,
    multiply,
    sum_numbers,
)

__all__ = ["REDIS_URL", "add", "app", "multiply", "sum_numbers"]
