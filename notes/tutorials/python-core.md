---
date updated: 2026-07-10
---

# Python 核心补缺

## typing

`typing.Annotated` 用来给类型附加元数据。类型检查器仍看到基础类型，框架可以读取元数据。

```python
from typing import Annotated, get_args, get_origin

UserId = Annotated[int, "positive database id"]

assert get_origin(UserId) is Annotated
assert get_args(UserId) == (int, "positive database id")
```

`@runtime_checkable` 让 `Protocol` 可以在运行时配合 `isinstance()` 做结构检查。

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Closer(Protocol):
    def close(self) -> None: ...


def close_if_needed(value: object) -> None:
    if isinstance(value, Closer):
        value.close()
```

## 装饰器

装饰器本质是接收函数并返回新函数。实际项目必须保留 `__name__`、docstring 和签名信息。

```python
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__}: {perf_counter() - start:.3f}s")

    return wrapper
```

## datetime

统一使用带时区的时间。存储用 UTC，展示时再转换到用户时区。

```python
from datetime import UTC, datetime
from zoneinfo import ZoneInfo

now = datetime.now(UTC)
shanghai = now.astimezone(ZoneInfo("Asia/Shanghai"))

text = shanghai.strftime("%Y-%m-%d %H:%M:%S %Z")
parsed = datetime.strptime("2026-07-10", "%Y-%m-%d").replace(tzinfo=UTC)
```

## 压缩与解压

常用 Linux 命令：

```bash
tar -czf archive.tar.gz notes
tar -xzf archive.tar.gz
zip -r notes.zip notes
unzip notes.zip
```

Python 中可用 `zipfile` 和 `tarfile`，脚本里优先用标准库而不是拼 shell。

## 队列

```python
from queue import LifoQueue, PriorityQueue, Queue

fifo: Queue[str] = Queue()
fifo.put("first")

lifo: LifoQueue[str] = LifoQueue()
lifo.put("last in first out")

priority: PriorityQueue[tuple[int, str]] = PriorityQueue()
priority.put((10, "low"))
priority.put((1, "high"))
```

- `Queue`：先进先出，生产者消费者。
- `LifoQueue`：后进先出，适合栈式任务。
- `PriorityQueue`：按优先级取任务。

## 不可变数据结构

标准库里先考虑 `tuple`、`frozenset`、`dataclasses.dataclass(frozen=True)`。需要高性能不可变映射时再使用 `immutables.Map`。

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int
```

## 迭代工具

`itertools` 适合无限序列、组合、分组和惰性管道。

```python
from itertools import chain, islice, pairwise

values = list(chain([1, 2], [3, 4]))
first_three = list(islice(range(100), 3))
pairs = list(pairwise(["a", "b", "c"]))
```

`more-itertools` 是第三方增强包，适合分块、窗口、去重和更复杂的迭代配方。

## 资源关闭

简单资源用 `with`，多个动态资源用 `ExitStack`，异步资源用 `AsyncExitStack`。

```python
from contextlib import ExitStack

paths = ["a.txt", "b.txt"]

with ExitStack() as stack:
    files = [stack.enter_context(open(path, encoding="utf-8")) for path in paths]
    data = [file.read() for file in files]
```

`atexit` 只适合兜底清理，不要依赖它做关键业务提交。

## 文件锁

跨进程写同一文件时需要文件锁。优先选成熟库，例如 `filelock` 或平台库；只在清楚平台差异时直接用 `fcntl`/`msvcrt`。

## bit、uuid、crc

- `bitarray`：紧凑存储大量布尔位，适合 bitmap、布隆过滤器等。
- `uuid6`：生成时间有序 UUID，适合需要索引局部性的 ID。
- `binascii.crc32`：快速校验数据是否变化，不是密码学哈希。

```python
from binascii import crc32

checksum = crc32(b"payload")
```

## 参考

- Python typing：<https://docs.python.org/3/library/typing.html>
- Python contextlib：<https://docs.python.org/3/library/contextlib.html>
- Python queue：<https://docs.python.org/3/library/queue.html>

