"""Celery producer 示例。"""

from __future__ import annotations

from celery import chain, chord, group

from python_notes.examples.task_queues.celery.tasks import add, multiply, sum_numbers


def submit_single_task() -> None:
    """提交一个普通异步任务并等待结果。"""
    result = add.apply_async(args=(4, 6), countdown=1)
    print("Task ID:", result.id)
    print("Result:", result.get(timeout=10))


def submit_workflow() -> None:
    """提交 chain、group、chord 工作流。"""
    chained = chain(add.s(2, 3), multiply.s(10)).apply_async()
    print("Chain Result:", chained.get(timeout=10))

    grouped = group(add.s(index, index + 1) for index in range(3)).apply_async()
    print("Group Result:", grouped.get(timeout=10))

    summarized = chord(
        [multiply.s(index, 2) for index in range(1, 4)],
        sum_numbers.s(),
    ).apply_async()
    print("Chord Result:", summarized.get(timeout=10))


def main() -> None:
    """运行 producer 示例。"""
    submit_single_task()
    submit_workflow()


if __name__ == "__main__":
    main()
