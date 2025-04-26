from celery import Celery

app = Celery(
    "tasks",
    broker="redis://43.156.74.18:6379/0",  # 无密码
    backend="redis://43.156.74.18:6379/0",  # 无密码
)


@app.task
def add(x, y):
    return x + y
