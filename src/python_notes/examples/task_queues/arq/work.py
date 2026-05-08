"""ARQ worker 示例。

启动命令:
    arq work.WorkerSettings
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any, Final
from urllib.parse import urlparse

from arq import cron, func
from arq.connections import RedisSettings
from arq.worker import Retry

DEFAULT_REDIS_URL: Final[str] = "redis://43.156.74.18:6379/0"


@dataclass(frozen=True)
class RedisConfig:
    """Redis 连接配置。

    Attributes:
        host: Redis 主机地址。
        port: Redis 端口。
        database: Redis 数据库编号。
        password: Redis 密码，未设置时为 ``None``。
    """

    host: str
    port: int
    database: int
    password: str | None = None

    def to_settings(self) -> RedisSettings:
        """转换为 ARQ 使用的 RedisSettings。

        Returns:
            可直接传给 ARQ worker 或 pool 的连接配置。
        """
        return RedisSettings(
            host=self.host,
            port=self.port,
            database=self.database,
            password=self.password,
        )


def redis_config_from_env() -> RedisConfig:
    """从环境变量读取 Redis 配置。

    环境变量 ``TASK_QUEUE_REDIS_URL`` 采用标准 Redis URL 格式，例如
    ``redis://:password@localhost:6379/0``。

    Returns:
        解析后的 Redis 连接配置。
    """
    url = urlparse(os.getenv("TASK_QUEUE_REDIS_URL", DEFAULT_REDIS_URL))
    return RedisConfig(
        host=url.hostname or "localhost",
        port=url.port or 6379,
        database=int(url.path.lstrip("/") or 0),
        password=url.password,
    )


async def startup(ctx: dict[str, Any]) -> None:
    """初始化 worker 上下文。

    Args:
        ctx: ARQ 注入的 worker 运行上下文。
    """
    ctx["processed_jobs"] = 0


async def shutdown(ctx: dict[str, Any]) -> None:
    """清理 worker 上下文。

    Args:
        ctx: ARQ 注入的 worker 运行上下文。
    """
    print(f"Processed jobs: {ctx.get('processed_jobs', 0)}")


async def add(ctx: dict[str, Any], a: int, b: int) -> int:
    """计算两个整数的和。

    Args:
        ctx: ARQ 注入的任务上下文。
        a: 第一个整数。
        b: 第二个整数。

    Returns:
        两个整数相加后的结果。
    """
    ctx["processed_jobs"] = ctx.get("processed_jobs", 0) + 1
    return a + b


async def multiply(ctx: dict[str, Any], a: int, b: int) -> int:
    """计算两个整数的乘积。

    Args:
        ctx: ARQ 注入的任务上下文。
        a: 第一个整数。
        b: 第二个整数。

    Returns:
        两个整数相乘后的结果。
    """
    ctx["processed_jobs"] = ctx.get("processed_jobs", 0) + 1
    return a * b


async def flaky_job(ctx: dict[str, Any], value: int) -> int:
    """演示基于重试次数的失败重试。

    Args:
        ctx: ARQ 注入的任务上下文，包含 ``job_try`` 等运行时信息。
        value: 需要处理的整数。

    Returns:
        输入整数的两倍。

    Raises:
        Retry: 前两次执行时触发延迟重试。
    """
    if ctx["job_try"] < 3:
        raise Retry(defer=1)
    return value * 2


async def heartbeat(ctx: dict[str, Any]) -> None:
    """定时输出 worker 心跳。

    Args:
        ctx: ARQ 注入的任务上下文。
    """
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
