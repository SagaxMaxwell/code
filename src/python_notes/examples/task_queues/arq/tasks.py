"""ARQ worker 示例。"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any, Final
from urllib.parse import urlparse

from arq import cron, func
from arq.connections import RedisSettings
from arq.worker import Retry

DEFAULT_REDIS_URL: Final[str] = "redis://localhost:6379/0"


@dataclass(frozen=True)
class RedisConfig:
    """Redis 连接配置。"""

    host: str
    port: int
    database: int
    password: str | None = None

    def to_settings(self) -> RedisSettings:
        """转为 ARQ RedisSettings。"""
        return RedisSettings(
            host=self.host,
            port=self.port,
            database=self.database,
            password=self.password,
        )


def redis_config_from_env() -> RedisConfig:
    """读取 TASK_QUEUE_REDIS_URL。"""
    url = urlparse(os.getenv("TASK_QUEUE_REDIS_URL", DEFAULT_REDIS_URL))
    return RedisConfig(
        host=url.hostname or "localhost",
        port=url.port or 6379,
        database=int(url.path.lstrip("/") or 0),
        password=url.password,
    )


async def startup(ctx: dict[str, Any]) -> None:
    """初始化 worker 上下文。"""
    ctx["processed_jobs"] = 0


async def shutdown(ctx: dict[str, Any]) -> None:
    """输出处理统计。"""
    print(f"Processed jobs: {ctx.get('processed_jobs', 0)}")


async def add(ctx: dict[str, Any], a: int, b: int) -> int:
    """求和。"""
    ctx["processed_jobs"] = ctx.get("processed_jobs", 0) + 1
    return a + b


async def multiply(ctx: dict[str, Any], a: int, b: int) -> int:
    """求积。"""
    ctx["processed_jobs"] = ctx.get("processed_jobs", 0) + 1
    return a * b


async def flaky_job(ctx: dict[str, Any], value: int) -> int:
    """前两次失败，第三次返回两倍值。"""
    if ctx["job_try"] < 3:
        raise Retry(defer=1)
    return value * 2


async def heartbeat(ctx: dict[str, Any]) -> None:
    """输出 worker 心跳。"""
    print("ARQ worker heartbeat")
    await asyncio.sleep(0)


class WorkerSettings:
    """ARQ worker 配置。"""

    functions = [
        func(add, name="add", keep_result=3600, timeout=10),
        func(multiply, name="multiply", keep_result=3600, timeout=10),
        func(flaky_job, name="flaky_job", keep_result=3600, timeout=15, max_tries=3),
    ]
    cron_jobs = [cron(heartbeat, minute={0, 30}, run_at_startup=True)]
    redis_settings = redis_config_from_env().to_settings()
    on_startup = startup
    on_shutdown = shutdown
    max_jobs = 10
