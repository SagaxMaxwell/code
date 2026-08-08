# 任务队列示例

这里存放和并发教程配套的可运行任务队列代码。Notebook 负责解释概念和 API，当前包只保留 worker、任务函数和 producer 示例。

## Celery

- 教程入口：[[../tutorials/concurrency/celery.ipynb|concurrency/celery]]
- [[celery/tasks.py|tasks]]: Celery 任务函数。
- [[celery/client.py|client]]: Celery producer 示例。

```zsh
celery -A python_notes.task_queues.celery.tasks worker --loglevel=info
python -m python_notes.task_queues.celery.client
```

## Dramatiq

- 教程入口：[[../tutorials/concurrency/dramatiq.ipynb|concurrency/dramatiq]]
- [[dramatiq/tasks.py|tasks]]: Dramatiq actor。
- [[dramatiq/client.py|client]]: Dramatiq producer 示例。

```zsh
dramatiq python_notes.task_queues.dramatiq.tasks
python -m python_notes.task_queues.dramatiq.client
```

## ARQ

- 教程入口：[[../tutorials/concurrency/arq.ipynb|concurrency/arq]]
- [[arq/tasks.py|tasks]]: ARQ 协程任务和 worker 配置。
- [[arq/client.py|client]]: ARQ producer 示例。

```zsh
arq python_notes.task_queues.arq.tasks.WorkerSettings
python -m python_notes.task_queues.arq.client
```
