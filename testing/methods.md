# 测试方法与用例设计

> 用途：用一个小型“产线配置字服务”串起常见测试概念和 pytest 写法。
> 适用类型：知识 / 实践
> 更新：2026-10-25

## 结论或简介

测试方法不是互斥标签：一个测试既可以是黑盒测试，也可以是集成测试和回归测试。实际工作中先明确测试目标，再选择测试层级、测试数据和验证方式。

示例服务负责校验配置字、调用设备写入并读取校验。它足够小，但能覆盖单元、白盒、黑盒、灰盒、集成、回归、边界值、等价类、异常注入和性能测试。

## 示例对象

### 被测代码

```python
from dataclasses import dataclass
from typing import Protocol


class Device(Protocol):
    def write_config(self, value: bytes) -> None: ...
    def read_config(self) -> bytes: ...


@dataclass
class ConfigService:
    device: Device

    def apply(self, value: bytes) -> None:
        if len(value) != 2:
            raise ValueError("config word must contain exactly 2 bytes")
        if value == b"\x00\x00":
            raise ValueError("config word cannot be zero")

        self.device.write_config(value)
        actual = self.device.read_config()
        if actual != value:
            raise RuntimeError("config word verification failed")
```

### 测试替身

```python
class FakeDevice:
    def __init__(self, value: bytes = b"\x00\x01") -> None:
        self.value = value
        self.write_count = 0

    def write_config(self, value: bytes) -> None:
        self.write_count += 1
        self.value = value

    def read_config(self) -> bytes:
        return self.value
```

## 测试分类

### 单元测试

只测试一个类或函数，依赖用 fake、mock 或 stub 隔离。

```python
def test_apply_writes_valid_config() -> None:
    device = FakeDevice()

    ConfigService(device).apply(b"\x01\x02")

    assert device.value == b"\x01\x02"
    assert device.write_count == 1
```

### 黑盒测试

只根据输入和输出设计用例，不关注内部实现。

```python
import pytest


@pytest.mark.parametrize(
    ("value", "expected_error"),
    [
        (b"", "exactly 2 bytes"),
        (b"\x01", "exactly 2 bytes"),
        (b"\x01\x02\x03", "exactly 2 bytes"),
        (b"\x00\x00", "cannot be zero"),
    ],
)
def test_apply_rejects_invalid_config(value: bytes, expected_error: str) -> None:
    with pytest.raises(ValueError, match=expected_error):
        ConfigService(FakeDevice()).apply(value)
```

### 白盒测试

根据代码分支和路径设计用例，目标是覆盖重要逻辑，而不只是覆盖正常输入。

本服务至少有三条路径：

```text
长度错误 → ValueError
全零配置 → ValueError
写入后读取不一致 → RuntimeError
写入并校验一致 → 成功
```

```python
class MismatchDevice(FakeDevice):
    def read_config(self) -> bytes:
        return b"\xff\xff"


def test_apply_rejects_device_mismatch() -> None:
    with pytest.raises(RuntimeError, match="verification failed"):
        ConfigService(MismatchDevice()).apply(b"\x01\x02")
```

### 灰盒测试

知道部分内部信息，但仍从外部行为验证。例如已知设备协议要求配置字固定 2 字节，于是重点检查长度、全零值和写后读回，但不依赖具体私有方法。

灰盒测试适合测试开发：利用协议、日志、状态机和数据格式等内部知识，设计更有针对性的黑盒用例。

### 集成测试

验证多个真实组件之间能否协同工作，例如 `ConfigService` 加真实 CAN/UDS adapter。不要把硬件测试误当成单元测试。

```python
def test_apply_with_fake_adapter() -> None:
    # 这里仍是可控的 adapter；接入真实设备时可放到 integration 标记下。
    device = FakeDevice()

    ConfigService(device).apply(b"\x10\x01")

    assert device.read_config() == b"\x10\x01"
```

真实设备集成测试可以单独标记：

```python
import pytest


@pytest.mark.integration
def test_apply_on_real_device(real_device) -> None:
    ConfigService(real_device).apply(b"\x10\x01")
```

### 回归测试

把已经发现并修复的问题固化成测试，防止后续重构再次引入。

```python
def test_regression_zero_config_is_rejected() -> None:
    """曾经出现全零配置被错误写入设备的问题。"""
    with pytest.raises(ValueError):
        ConfigService(FakeDevice()).apply(b"\x00\x00")
```

回归测试不等于某种测试层级：它可以是单元测试、集成测试，也可以是端到端测试。

## 测试数据设计

### 等价类

把预期行为相同的输入划为一类，每类选代表值，减少无效重复。

| 等价类 | 示例 | 预期 |
| --- | --- | --- |
| 合法长度、非零 | `b"\x01\x02"` | 成功 |
| 空输入 | `b""` | 长度错误 |
| 长度不足 | `b"\x01"` | 长度错误 |
| 长度超出 | `b"\x01\x02\x03"` | 长度错误 |
| 合法长度但业务无效 | `b"\x00\x00"` | 拒绝 |

### 边界值

重点测试规则边界及其相邻值。本例长度要求是 2：

```python
@pytest.mark.parametrize("value", [b"", b"\x01", b"\x01\x02\x03"])
def test_length_boundaries(value: bytes) -> None:
    with pytest.raises(ValueError):
        ConfigService(FakeDevice()).apply(value)
```

通常至少覆盖：最小值、最小值前后、最大值、最大值前后，以及空值、零值和重复值。

## 异常注入

主动让依赖失败，验证系统是否正确传播、转换、重试或清理资源。

```python
class FailingDevice:
    def write_config(self, value: bytes) -> None:
        raise TimeoutError("device write timeout")

    def read_config(self) -> bytes:
        raise AssertionError("read should not be called")


def test_device_timeout_is_not_silently_ignored() -> None:
    with pytest.raises(TimeoutError, match="timeout"):
        ConfigService(FailingDevice()).apply(b"\x01\x02")
```

常见注入点：超时、连接断开、错误响应、返回空数据、写入后读回不一致、磁盘满、消息重复和进程中断。

## 性能测试

性能测试应先定义指标和数据规模；不要用小样本的单次耗时得出结论。

```python
import time


def test_apply_latency() -> None:
    device = FakeDevice()
    service = ConfigService(device)
    start = time.perf_counter()

    for _ in range(1_000):
        service.apply(b"\x01\x02")

    elapsed = time.perf_counter() - start
    assert elapsed < 0.5
```

这个例子只是简单基准，不等于正式性能测试。正式测试还应记录吞吐量、P95/P99 延迟、资源占用、并发数和错误率，并避免把真实硬件的网络波动混入纯代码基准。

## 路径与组合测试

路径测试关注控制流是否覆盖；组合测试关注多个条件同时变化时是否仍正确。

本例可组合：

```text
输入长度：正确 / 错误
配置值：普通 / 全零
设备行为：成功 / 超时 / 读回不一致
```

不要机械地穷举所有组合。优先覆盖高风险组合，例如“合法输入 + 写入成功 + 读回不一致”，以及“设备超时 + 不应继续读取”。

## 测试层级的选择

| 测试 | 主要回答的问题 | 运行特点 |
| --- | --- | --- |
| 单元测试 | 一个函数或类是否正确 | 快、稳定、数量多 |
| 集成测试 | 多个组件能否协作 | 较慢，需要真实或接近真实依赖 |
| 端到端测试 | 用户或产线流程是否可用 | 最接近真实，但成本最高 |
| 回归测试 | 已修复问题是否再次出现 | 按历史缺陷持续积累 |

推荐比例不是硬性规则，但通常应让大多数测试停留在快速的单元层，少量关键流程使用集成和端到端测试。

## pytest 运行

将代码保存为 `test_config_service.py` 后运行：

```bash
pytest -q test_config_service.py
pytest -q -m integration
```

如果使用 `integration` 标记，在 `pyproject.toml` 中声明：

```toml
[tool.pytest.ini_options]
markers = [
    "integration: requires multiple components or a real device",
]
```

## pytest 常用能力

### Fixture

fixture 负责准备和清理测试依赖，例如客户端、临时目录和数据库连接。

```python
import pytest


@pytest.fixture
def user_payload() -> dict[str, str]:
    return {"name": "Alice", "email": "alice@example.com"}


@pytest.fixture
def resource():
    item = open_resource()
    yield item
    item.close()
```

`yield` 前准备资源，`yield` 后清理资源。需要共享资源时再考虑 `scope="module"` 或 `scope="session"`，有状态的设备通常使用更小的范围。

### 参数化

同一测试逻辑需要验证多组输入时，优先使用参数化：

```python
@pytest.mark.parametrize(
    ("raw", "expected"),
    [(" A ", "a"), ("Bob", "bob")],
)
def test_normalize(raw: str, expected: str) -> None:
    assert raw.strip().lower() == expected
```

### Hook 与插件

fixture 解决“用例需要什么资源”；hook 解决“在 pytest 哪个执行阶段接入逻辑”。常见 hook 包括 `pytest_addoption`、`pytest_configure`、`pytest_collection_modifyitems` 和 `pytest_sessionfinish`。

常用插件：

| 插件 | 作用 |
| --- | --- |
| `pytest-cov` | 覆盖率 |
| `pytest-xdist` | 并行执行 |
| `pytest-timeout` | 防止用例卡死 |
| `pytest-asyncio` | 异步测试 |
| `pytest-benchmark` | 性能基准 |

## 测试框架分层

- 单元测试：函数、类和纯业务逻辑。
- 集成测试：数据库、缓存、消息队列、第三方 API 或真实设备。
- API 测试：接口契约、状态码和错误结构。
- 端到端测试：真实业务流程，数量少但覆盖关键路径。

测试数据、断言、客户端、设备适配和报告应分开，避免测试脚本堆成不可维护的流程代码。

## 常见边界

- 单元测试不要连接真实设备；真实设备测试应单独标记并控制环境。
- 覆盖率高不代表质量高，仍要检查断言是否验证了真正的业务结果。
- 测试失败时先区分产品缺陷、测试缺陷、环境故障和数据问题。
- 性能测试要固定数据规模、环境和指标，否则结果不可比较。
- 异常测试不仅要断言“抛错”，还要确认没有继续执行危险操作。
