# 任务队列示例

这里存放和教程配套的可运行任务队列代码。

## Celery

- [[celery/tasks.py|tasks]]: Celery 任务函数。
- [[celery/client.py|client]]: Celery producer 示例。

```zsh
celery -A python_notes.task_queues.celery.tasks worker --loglevel=info
python -m python_notes.task_queues.celery.client
```

## Dramatiq

- [[dramatiq/tasks.py|tasks]]: Dramatiq actor。
- [[dramatiq/client.py|client]]: Dramatiq producer 示例。

```zsh
dramatiq python_notes.task_queues.dramatiq.tasks
python -m python_notes.task_queues.dramatiq.client
```

## ARQ

- [[arq/tasks.py|tasks]]: ARQ 协程任务和 worker 配置。
- [[arq/client.py|client]]: ARQ producer 示例。

```zsh
arq python_notes.task_queues.arq.tasks.WorkerSettings
python -m python_notes.task_queues.arq.client
```
