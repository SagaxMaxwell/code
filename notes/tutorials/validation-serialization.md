---
date updated: 2026-07-10
---

# 校验与序列化

## Pydantic v2 心智模型

Pydantic 适合边界层：HTTP 请求、配置文件、消息队列 payload、外部 API 响应。业务内部不要把所有对象都做成 Pydantic 模型，否则会把校验层和领域逻辑绑死。

```python
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class Item(BaseModel):
    sku_id: Annotated[str, Field(min_length=1)]
    quantity: Annotated[int, Field(gt=0)]

    @field_validator("sku_id", mode="before")
    @classmethod
    def strip_sku(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value
```

## before / plain validator

- `mode="before"`：在类型转换前清洗输入。
- `mode="after"`：拿到已校验类型后做业务规则。
- plain validator：完全接管校验流程，慎用，适合特殊外部类型。

## 自定义 core schema

`__get_pydantic_core_schema__` 用于让 Pydantic 理解自定义类型。只有当普通 validator 不够表达时才需要。

```python
from pydantic_core import core_schema


class UpperCode(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.no_info_after_validator_function(
            lambda value: cls(value.upper()),
            core_schema.str_schema(),
        )
```

## serializer

序列化负责把内部类型输出成 JSON 友好结构。

```python
from decimal import Decimal

from pydantic import BaseModel, field_serializer


class Price(BaseModel):
    amount: Decimal

    @field_serializer("amount")
    def dump_amount(self, value: Decimal) -> str:
        return f"{value:.2f}"
```

## msgspec

`msgspec` 适合高性能 JSON/MessagePack 编解码，尤其是大量结构化数据。它比 Pydantic 更偏序列化和数据交换，Pydantic 更偏边界校验与错误解释。

```python
import msgspec


class Event(msgspec.Struct):
    event_type: str
    sku_id: str
    quantity: int


event = msgspec.json.decode(
    b'{"event_type":"order_paid","sku_id":"SKU-8","quantity":2}',
    type=Event,
)
```

## 文件解析

| 工具 | 用法 |
| --- | --- |
| `lxml` | XML/HTML 解析、XPath |
| `ruamel.yaml` | 需要保留注释和格式的 YAML |
| `tomllib` | Python 3.11+ 读取 TOML |
| `tomli-w` | 写 TOML |
| `python-dotenv` | 本地开发加载 `.env` |

配置读取建议顺序：默认值、配置文件、环境变量、命令行参数。密钥不要提交进仓库。

## 参考

- Pydantic 官方文档：<https://docs.pydantic.dev/latest/>
- msgspec 官方文档：<https://jcristharif.com/msgspec/>
- Python tomllib：<https://docs.python.org/3/library/tomllib.html>

