---
date updated: 2026-10-26T13:13
date created: 2026-10-25T14:34
---

# 设计取舍

## 什么时候绑定参数，什么时候传参数

判断核心：**对象生命周期内不变的上下文，在构造时绑定；每次调用可能变化的数据，通过方法传入。**

| 情况            | 做法     | 示例                  |
| ------------- | ------ | ------------------- |
| 参数决定对象代表谁     | 构造时绑定  | 一个 `MdcPort` 固定对应主面 |
| 多个方法反复使用同一个值  | 构造时绑定  | 车型、连接、默认诊断配置        |
| 参数与其他依赖必须保持一致 | 构造时绑定  | 主面 SSH 连接与主面 UDS 通道 |
| 每次调用的数据不同     | 方法传参   | 本次写入的配置字、VIN、密钥     |
| 调用者需要明确选择目标   | 方法传参   | 查询主面或副面的状态          |
| 一个流程同时操作多个目标  | 分别注入对象 | 同时注入主面和副面 `MdcPort` |

构造时绑定：

```python
class MdcCommander:
    def __init__(self, connection: SshConnection) -> None:
        self._connection = connection

    def wait_until_reachable(self, timeout: float) -> None: ...


primary_mdc = MdcCommander(primary_connection)
secondary_mdc = MdcCommander(secondary_connection)
```

方法传参：

```python
class ElectronicInspectionService:
    def write_vin(self, vin: bytes) -> None: ...
```

不要重复表达同一信息：

```python
# 不推荐：对象已经绑定主面，调用时又允许传副面。
primary_mdc.wait_until_reachable(
    plane=MdcPlane.SECONDARY,
    timeout=45.0,
)
```

快速判断：

> 对象活着期间不应改变，就绑定；每次调用可以不同，就传参。

## 什么时候把函数参数封装成类

判断核心：**参数类应该表达一个完整概念，而不只是为了缩短函数签名。**

| 适合封装           | 不必封装                           |
| -------------- | ------------------------------ |
| 参数总是一起出现、一起变化  | 只有一两个含义清楚的参数                   |
| 参数组合有校验规则      | 参数彼此没有关系                       |
| 多个流程都会复用这组参数   | 参数只在一个简单函数中使用                  |
| 它们能形成明确的业务概念   | 类名只能叫 `Options`、`Params` 等模糊名称 |
| 参数较多，已经影响调用可读性 | 封装后只是多构造一个对象                   |

不必封装：

```python
def reset_and_wait(
    self,
    reset_type: EcuResetType = EcuResetType.HARD_RESET,
    timeout: float = 45.0,
) -> bytes: ...
```

这两个参数数量少、含义清楚，直接传入更简单。

适合封装：

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class DiagnosticAccess:
    session_type: int
    seed_sub_function: int | None = None


def write_certificate(
    self,
    certificate: bytes,
    access: DiagnosticAccess,
) -> None: ...
```

`session_type` 和 `seed_sub_function` 共同表达“诊断访问条件”，还可以被多个业务复用。

参数很多时，不要直接创建万能参数包，应先按概念拆分：

```python
@dataclass(frozen=True)
class CertificateProvisioningSpec:
    access: DiagnosticAccess
    write_identifier: int
    verify_identifier: int
    reset: ResetPolicy
```

快速判断：

> 能准确命名、共同变化、需要复用或校验，就封装；只是为了少写几个参数，就不封装。

## 什么时候共用异常，什么时候拆分异常

判断核心：**错误信息用于告诉人哪里出错；异常类型用于让程序决定如何处理。**

| 情况             | 做法               | 示例                                                        |
| -------------- | ---------------- | --------------------------------------------------------- |
| 错误来源不同，但处理方式相同 | 共用异常，使用消息和属性描述细节 | VIN、配置字回读不一致都抛 `VerificationError`                        |
| 调用方需要采取不同恢复策略  | 拆分异常类型           | 超时可重试，连接失败需重连                                             |
| 仅操作名称或输入值不同    | 不拆分              | `operation="write_vin"` 与 `operation="write_config_word"` |
| 错误语义不同         | 拆分               | 校验失败、安全访问失败、设备未就绪                                         |
| 只是编程错误或参数非法    | 优先使用内置异常         | `TypeError`、`ValueError`                                  |

业务不同，不代表必须各自定义一个异常。配置字、VIN、密钥写入后的回读值不一致，本质上都可以属于“业务结果校验失败”：

```python
class ElectronicInspectionError(Exception):
    pass


class VerificationError(ElectronicInspectionError):
    def __init__(
        self,
        operation: str,
        expected: bytes,
        actual: bytes,
    ) -> None:
        self.operation = operation
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"{operation} verification failed: "
            f"expected={expected.hex()}, actual={actual.hex()}"
        )
```

```python
raise VerificationError(
    operation="write_config_word",
    expected=config_word.value,
    actual=actual,
)
```

只有调用方需要区别处理时，才值得拆分：

```python
class SecurityAccessError(ElectronicInspectionError):
    pass


class DeviceNotReadyError(ElectronicInspectionError):
    pass
```

```python
try:
    service.write_config_word(config_word)
except SecurityAccessError:
    check_security_configuration()
except DeviceNotReadyError:
    reconnect_device()
except VerificationError:
    record_test_failure()
```

不要通过解析消息决定程序行为：

```python
# 不推荐：错误消息不是稳定的程序接口。
except ElectronicInspectionError as error:
    if "timeout" in str(error):
        retry()
```

分层时可以采用以下边界：

| 层级 | 异常职责 |
| --- | --- |
| `domain` | 领域规则或值对象约束失败 |
| `application` | 上层需要识别和处理的业务、Port 契约错误 |
| `infrastructure` | 动态库、厂商返回码、协议实现等技术错误 |

基础设施可以定义 `ZcanError` 等厂商异常，并在适配器边界按需转换成 application 能理解的异常。无需为每个 SDK 函数建立一个异常类；如果处理方式相同，一个异常类型配合清楚的操作信息即可。

另外，被测对象不符合预期不一定都是程序异常。能够完整得到测试结果时，可以返回结果并由 pytest 判定失败；只有流程无法继续、前置条件不满足或无法可靠得到结果时，才更适合抛异常。

快速判断：

> 只需要让人知道哪里错了，就共用异常并补充信息；需要让程序采取不同措施，才拆分异常类型。

## 一分钟检查清单

- 这是本次输入，还是对象固定上下文？
- 调用期间会不会变化？
- 多个参数是否构成一个可以准确命名的概念？
- 封装后是否减少错误或重复，而不只是转移复杂度？
- 当前是否已有真实需求，而不是只为“以后可能用到”预留？
- 异常差异是给人定位，还是要让程序采取不同措施？
