# 任务队列示例

这里存放和教程配套的可运行任务队列代码。

## Celery

```zsh
celery -A python_notes.examples.task_queues.celery.work worker --loglevel=info
python -m python_notes.examples.task_queues.celery.job
```

## Dramatiq

```zsh
dramatiq python_notes.examples.task_queues.dramatiq.work
python -m python_notes.examples.task_queues.dramatiq.job
```

## ARQ

```zsh
arq python_notes.examples.task_queues.arq.work.WorkerSettings
python -m python_notes.examples.task_queues.arq.job
```
