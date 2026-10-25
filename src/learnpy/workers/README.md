# 任务队列

与并发教程配套的 Celery、Dramatiq 和 ARQ 示例。

```bash
celery -A learnpy.workers.celery.tasks worker --loglevel=info
dramatiq learnpy.workers.dramatiq.tasks
arq learnpy.workers.arq.tasks.WorkerSettings
```
