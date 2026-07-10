"""Dramatiq producer 示例。"""

from __future__ import annotations

import dramatiq

from python_notes.examples.task_queues.dramatiq.tasks import add, multiply


def submit_single_task() -> None:
    """提交一个普通异步任务并等待结果。"""
    message = add.send(3, 5)
    result = message.get_result(block=True, timeout=10_000)
    print("Message ID:", message.message_id)
    print("Result:", result)


def submit_workflow() -> None:
    """提交 pipeline 工作流。"""
    workflow = dramatiq.pipeline(
        [
            add.message(2, 3),
            multiply.message(10),
        ]
    ).run()
    print("Pipeline Result:", workflow.get_result(block=True, timeout=10_000))


def main() -> None:
    """运行 producer 示例。"""
    submit_single_task()
    submit_workflow()


if __name__ == "__main__":
    main()
