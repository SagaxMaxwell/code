---
date updated: 2026-07-10
---

# Web API 与应用

## API 层职责

API 层负责协议和边界，不负责堆业务细节：

- 解析 HTTP 请求、鉴权、限流。
- 用 Pydantic 或 dataclass 校验输入输出。
- 调用内部 service / scheduler / domain 对象。
- 统一异常结构、日志和追踪 ID。

服务层负责业务规则。这样 CLI、定时任务、Gradio UI 和 FastAPI 都能复用同一套核心逻辑。

## FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class PredictRequest(BaseModel):
    text: str = Field(min_length=1)


class PredictResponse(BaseModel):
    label: str
    score: float


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    return PredictResponse(label="ok", score=0.99)
```

前后端模型必须一致。实践上有三种方式：

- 后端导出 OpenAPI，让前端生成客户端类型。
- 把 JSON Schema 作为契约，前后端共同校验。
- 在单仓库中共享 schema 定义或生成产物。

## Gradio

Gradio 适合模型 Demo、内部工具和低成本人工评测。复杂后台业务仍然放 service 层，UI 只绑定输入输出。

```python
import gradio as gr


def greet(name: str) -> str:
    return f"Hello {name.strip() or 'world'}"


with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output")
    name.change(greet, inputs=name, outputs=output)
```

常见事件：

- `change`：值变化后触发，适合输入框、下拉框联动。
- `input`：用户输入时触发，适合即时反馈。
- `select`：用户选择列表、表格、图库元素时触发。
- `click`：按钮操作。

刷新文本组件时，输出函数必须返回新的值。需要清空就返回空字符串 `""`。

## Reflex

Reflex 用 Python 写全栈 UI，适合希望用 Python 管理前端状态的应用。学习重点是状态类、事件处理、组件组合和部署边界。不要把它和 FastAPI/Gradio混为一谈：FastAPI 是 API 框架，Gradio 是模型/工具 UI，Reflex 是更完整的 Web 应用框架。

## 服务边界建议

- API schema 不直接暴露数据库 ORM 对象。
- 后端 response model 与前端类型保持同源。
- 长任务不要阻塞请求线程，交给队列或任务调度器。
- 统一错误码、错误消息和日志字段。

## 参考

- FastAPI 官方文档：<https://fastapi.tiangolo.com/>
- Gradio 官方文档：<https://www.gradio.app/docs/>
- Reflex 官方文档：<https://reflex.dev/docs/>

