---
date updated: 2026-07-10
---

# 测试与 pytest

## 测试类型

| 类型 | 核心问题 | 常见用法 |
| --- | --- | --- |
| 白盒测试 | 代码路径是否覆盖 | 分支、异常、边界条件 |
| 黑盒测试 | 输入输出是否符合需求 | 等价类、边界值、场景用例 |
| 灰盒测试 | 结合接口行为和内部结构 | API、数据库、副作用 |
| 静态测试 | 不运行代码能否发现问题 | Ruff、mypy、代码评审 |
| 动态测试 | 运行后行为是否正确 | 单元、集成、E2E |

用例设计先从风险开始：钱、权限、数据丢失、并发、超时、外部依赖、边界输入。每个用例写清楚前置条件、步骤、断言和清理方式。

## pytest 基础

```python
def normalize_name(value: str) -> str:
    return value.strip().lower()


def test_normalize_name() -> None:
    assert normalize_name("  Alice ") == "alice"
```

常用命令：

```bash
pytest
pytest -q
pytest tests/test_user.py::test_create_user
pytest -k "user and not slow"
pytest -m integration
```

## fixture

fixture 负责准备和清理测试依赖。不要在测试函数里重复创建数据库连接、临时目录或客户端。

```python
import pytest


@pytest.fixture
def user_payload() -> dict[str, str]:
    return {"name": "Alice", "email": "alice@example.com"}


def test_payload_has_email(user_payload: dict[str, str]) -> None:
    assert "@" in user_payload["email"]
```

需要清理资源时使用 `yield`：

```python
@pytest.fixture
def resource():
    item = open_resource()
    yield item
    item.close()
```

## 参数化

```python
import pytest


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (" A ", "a"),
        ("Bob", "bob"),
    ],
)
def test_normalize_cases(raw: str, expected: str) -> None:
    assert raw.strip().lower() == expected
```

如果中文参数名显示为转义，可在 `pytest.ini` 或 `pyproject.toml` 中设置：

```toml
[tool.pytest.ini_options]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support = true
```

## 命令行参数与 hook

`pytest_addoption` 用来添加自定义参数，`pytest_generate_tests` 用来动态生成参数。

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--env", default="local", choices=["local", "staging"])


def pytest_generate_tests(metafunc):
    if "env_name" in metafunc.fixturenames:
        env_name = metafunc.config.getoption("--env")
        metafunc.parametrize("env_name", [env_name])
```

pytest hook 是插件机制的核心。常用 hook：

- `pytest_configure`：注册 marker、初始化配置。
- `pytest_collection_modifyitems`：修改收集到的用例顺序、marker 或跳过逻辑。
- `pytest_runtest_setup`：用例运行前检查环境。
- `pytest_sessionfinish`：测试结束后汇总或清理。

## 常用插件

| 插件 | 作用 |
| --- | --- |
| `pytest-cov` | 覆盖率 |
| `pytest-xdist` | 并行执行 |
| `pytest-asyncio` | async 测试 |
| `pytest-timeout` | 防止测试卡死 |
| `pytest-repeat` | 重复执行定位偶发问题 |
| `pytest-benchmark` | 性能基准 |
| `pytest-json-report` | JSON 报告 |
| `pytest-metadata` | 报告元数据 |
| `pytest-flask` / `pytest-django` | 框架集成 |
| `pytest-md-report` | Markdown 报告 |

`pytest-pep8` 不建议作为新项目选择。现代项目通常用 Ruff 做 lint 和格式检查，再把测试交给 pytest。

## 日志配置

```toml
[tool.pytest.ini_options]
log_cli = true
log_cli_level = "INFO"
log_cli_format = "%(asctime)s %(levelname)s %(name)s: %(message)s"
```

## 自动化测试框架分层

- 单元测试：函数、类、纯业务逻辑。
- 集成测试：数据库、缓存、消息队列、第三方 API。
- API 测试：HTTP 接口契约、状态码、错误结构。
- E2E 测试：浏览器真实流程，数量要少，覆盖关键路径。
- 模块化测试框架：把数据、断言、页面对象、客户端和报告拆开，避免测试脚本堆成流程代码。

## 参考

- pytest 官方文档：<https://docs.pytest.org/en/stable/>

