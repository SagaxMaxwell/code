---
date updated: 2026-07-26
---

## FastAPI 教程

### 适合场景

FastAPI 适合写类型清晰、接口契约明确的 Python HTTP API。它把 Starlette 的 ASGI 能力、Pydantic 的数据校验和 OpenAPI 文档生成组合在一起，适合后端服务、模型推理接口、内部平台 API 和前后端分离项目。

不建议把所有业务逻辑都写进路由函数。路由层只处理 HTTP 边界，真正的业务规则放到 service、domain 或 repository 层，便于 CLI、定时任务和测试复用。

### 安装与启动

使用 `uv`：

```bash
uv add "fastapi[standard]"
uv run fastapi dev app/main.py
```

只想直接用 ASGI Server 时：

```bash
uv add fastapi uvicorn
uv run uvicorn app.main:app --reload
```

`fastapi dev` 适合本地开发，`uvicorn app.main:app --reload` 是更通用的启动方式。生产环境不要开 `--reload`。

### 最小应用

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI(title="Task API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
```

启动后访问：

- API：`http://127.0.0.1:8000/health`
- Swagger UI：`http://127.0.0.1:8000/docs`
- ReDoc：`http://127.0.0.1:8000/redoc`
- OpenAPI JSON：`http://127.0.0.1:8000/openapi.json`

### 请求参数

路径参数用于定位资源，查询参数用于筛选、分页和开关类选项，请求体用于提交结构化数据。

```python
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    priority: int = Field(default=3, ge=1, le=5)
    done: bool = False


class TaskRead(BaseModel):
    id: int
    title: str
    priority: int
    done: bool


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int) -> TaskRead:
    return TaskRead(id=task_id, title="write docs", priority=2, done=False)


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(
    keyword: Annotated[str | None, Query(max_length=50)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[TaskRead]:
    return [
        TaskRead(id=1, title=keyword or "write docs", priority=2, done=False)
    ][:limit]


@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate) -> TaskRead:
    return TaskRead(id=1, **payload.model_dump())
```

要点：

- 类型标注会参与参数解析、校验和文档生成。
- `Field()` 用在 Pydantic 模型字段上。
- `Query()`、`Path()`、`Header()`、`Cookie()` 用在 HTTP 参数上。
- `response_model` 控制返回结构，不要直接暴露 ORM 对象。
- Pydantic v2 中常用 `model_dump()` 把模型转成字典。

### 状态码与异常

业务错误要变成稳定的 HTTP 状态码和错误结构，不要直接返回字符串。

```python
from fastapi import HTTPException, status


TASKS = {1: {"id": 1, "title": "write docs", "priority": 2, "done": False}}


@app.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(task_id: int) -> TaskRead:
    task = TASKS.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found",
        )
    return TaskRead(**task)
```

实践建议：

- 资源不存在用 `404`。
- 参数格式错误让 FastAPI 自动返回 `422`。
- 未登录用 `401`，无权限用 `403`。
- 创建成功用 `201`，删除成功可用 `204`。

### 依赖注入

依赖注入适合放认证、数据库会话、配置读取、分页参数和可替换的外部客户端。

```python
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status


class CurrentUser(BaseModel):
    username: str
    is_admin: bool = False


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    if authorization != "Bearer dev-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )
    return CurrentUser(username="alice")


@app.get("/me", response_model=CurrentUser)
def read_me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    return user
```

依赖函数可以继续依赖其他依赖。复杂项目里常见层次是：

- `get_settings()`：读取配置。
- `get_db()`：创建并清理数据库会话。
- `get_current_user()`：解析认证信息。
- `require_admin()`：检查权限。

### 路由拆分

接口变多后用 `APIRouter` 拆分模块。

```python
# app/routers/tasks.py
from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def list_tasks() -> list[dict[str, str]]:
    return [{"title": "write docs"}]
```

```python
# app/main.py
from fastapi import FastAPI

from app.routers import tasks

app = FastAPI(title="Task API")
app.include_router(tasks.router)
```

推荐结构：

```text
app/
  main.py
  routers/
    tasks.py
    users.py
  schemas.py
  services.py
  dependencies.py
tests/
  test_tasks.py
```

规模继续变大时，可以按业务域拆成 `app/tasks/router.py`、`app/tasks/schemas.py`、`app/tasks/service.py`。

### 同步与异步

FastAPI 支持 `def` 和 `async def`：

- 调用同步数据库驱动、同步 SDK 或 CPU 计算时，用 `def`。
- 调用异步数据库驱动、异步 HTTP 客户端或异步队列时，用 `async def` 并 `await`。
- 不要在 `async def` 里直接调用阻塞 IO；这会阻塞事件循环。
- CPU 密集型任务不要放请求线程里跑，交给任务队列或后台作业。

```python
import httpx


@app.get("/external")
async def call_external() -> dict[str, object]:
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get("https://example.com")
    return {"status_code": response.status_code}
```

### 测试

FastAPI 可以用 `TestClient` 直接测试 ASGI 应用，不需要真的启动端口。

```python
# tests/test_tasks.py
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task() -> None:
    response = client.post(
        "/tasks",
        json={"title": "write docs", "priority": 2},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "write docs"
```

测试重点：

- 正常路径、参数缺失、参数越界、权限错误、资源不存在。
- `response_model` 是否过滤了不该暴露的字段。
- 依赖注入是否能替换外部服务和数据库。
- 错误响应格式是否稳定。

### 常见问题

- 把 ORM 模型当 API schema：会把数据库结构泄漏到接口层。
- 返回未校验的字典：接口文档和真实返回容易漂移。
- 在路由函数里堆业务逻辑：测试困难，复用困难。
- 在请求里跑长任务：请求超时后状态难追踪。
- 混用同步和异步客户端：容易造成连接泄漏或事件循环阻塞。

### 参考

- FastAPI First Steps：<https://fastapi.tiangolo.com/tutorial/first-steps/>
- FastAPI Request Body：<https://fastapi.tiangolo.com/tutorial/body/>
- FastAPI Dependencies：<https://fastapi.tiangolo.com/tutorial/dependencies/>
- FastAPI Testing：<https://fastapi.tiangolo.com/tutorial/testing/>
