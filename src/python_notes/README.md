# python_notes 包

这是项目的可安装 Python 包。每个一级目录对应一个独立模块，模块下面再放 notebook 教程、练习、资源或可运行工具代码。

## 模块

- [[tutorials/README|tutorials]]: Python 基础、数据分析、标准库工具、并发、应用、自动化、算法和机器学习教程。
- [[exercises/README|exercises]]: 基础练习、阶段测评、数据练习和综合项目。
- [[task_queues/README|task_queues]]: Celery、Dramatiq 和 ARQ 的 worker/client 可运行代码。
- [[resources/README|resources]]: notebook 引用的数据集和图片资源。

## 边界

- `tutorials` 负责教学解释和可复制示例。
- `exercises` 负责训练题、测评题和项目练习。
- `task_queues` 负责能被 `python -m` 或 worker 命令直接运行的代码。
- `resources` 只保存静态资源，不放教程正文。
