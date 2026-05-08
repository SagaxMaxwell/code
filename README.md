# Python Notes

这个项目整理为 Python 工具教程、并发教程、算法基础和算法题库几个模块。

## 目录结构

```text
.
├── src/
│   └── python_notes/
│       ├── tutorials/
│       │   ├── algorithms/          # 算法基础与算法题
│       │   ├── concurrency/         # 并发、异步、分布式计算教程
│       │   ├── data_structures/     # 数据结构补充
│       │   └── python_tools/        # Python 标准库和常用工具
│       └── examples/
│           ├── basic/               # 基础 Python 脚本示例
│           └── task_queues/         # Celery、Dramatiq、ARQ 示例
└── tests/                           # 包结构和导入测试
```

## 模块说明

- `src/python_notes/tutorials/algorithms/patterns.ipynb`: 常用算法模式，如滑动窗口、二分、DFS/BFS、动态规划、排序等。
- `src/python_notes/tutorials/algorithms/problems.ipynb`: 经典算法题库，包含 LeetCode 和 HuaWei OD 题目。
- `src/python_notes/tutorials/data_structures/advanced_structures.ipynb`: 数据结构和结构化工具补充，如 `bisect`、`OrderedDict`。
- `src/python_notes/tutorials/python_tools/stdlib_tools.ipynb`: Python 工具教程，包含 `math`、`cmath`、`decimal`、`fractions`、`calendar`、`sched` 和 APScheduler。
- `src/python_notes/tutorials/concurrency/concurrency.ipynb`: 并发编程教程，包含 threading、multiprocessing、asyncio、Ray、Dask 和任务队列对比。
- `src/python_notes/examples/task_queues/`: 任务队列可运行示例，包含 Celery、Dramatiq、ARQ。
