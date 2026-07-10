# 任务队列示例

这里存放和教程配套的可运行任务队列代码。

## Celery

```zsh
celery -A python_notes.examples.task_queues.celery.tasks worker --loglevel=info
python -m python_notes.examples.task_queues.celery.client
```

## Dramatiq

```zsh
dramatiq python_notes.examples.task_queues.dramatiq.tasks
python -m python_notes.examples.task_queues.dramatiq.client
```

## ARQ

```zsh
arq python_notes.examples.task_queues.arq.tasks.WorkerSettings
python -m python_notes.examples.task_queues.arq.client
```
