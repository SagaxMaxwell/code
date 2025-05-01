import dramatiq
from dramatiq.brokers.redis import RedisBroker

# 配置 Redis 作为 broker（默认连接 redis://localhost:6379/0）
redis_broker = RedisBroker(url="redis://43.156.74.18:6379/0")
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def add(x, y):
    print(f"Result: {x + y}")
