# Python Notes

这个项目整理为 Python 基础教程、数据分析教程、Python 工具教程、并发教程、Web 应用教程、算法基础、算法题库和配套练习几个模块。

## 目录结构

```text
.
├── src/
│   └── python_notes/
│       ├── tutorials/
│       │   ├── algorithms/          # 算法基础与算法题
│       │   ├── concurrency/         # 并发、异步、分布式计算教程
│       │   ├── data_analysis/       # NumPy、Pandas、Matplotlib 教程
│       │   ├── data_structures/     # 数据结构补充
│       │   ├── machine_learning/    # 机器学习 PDF 资料
│       │   ├── python_foundations/  # Python 基础语法教程
│       │   ├── python_tools/        # Python 标准库和常用工具
│       │   ├── web_apps/            # Gradio、Streamlit 数据应用教程
│       │   └── web_automation/      # Selenium Web 自动化教程
│       ├── exercises/               # Python 基础、数据分析、测评和项目练习
│       ├── resources/               # 图片、数据集和 PDF 参考资料
│       └── examples/
│           ├── basic/               # 基础 Python 脚本示例
│           └── task_queues/         # Celery、Dramatiq、ARQ 示例
└── tests/                           # 包结构和导入测试
```

## 模块说明

- `src/python_notes/tutorials/algorithms/patterns.ipynb`: 常用算法模式，如滑动窗口、二分、DFS/BFS、动态规划、排序等。
- `src/python_notes/tutorials/algorithms/problems.ipynb`: 经典算法题库，包含 LeetCode 和 HuaWei OD 题目。
- `src/python_notes/tutorials/python_foundations/`: Python 基础语法教程，包含数据类型、函数、面向对象、文件系统等。
- `src/python_notes/tutorials/data_analysis/`: 数据分析教程，包含 NumPy、Pandas 和 Matplotlib。
- `src/python_notes/tutorials/machine_learning/`: 机器学习 PDF 资料，包含回归、逻辑回归、朴素贝叶斯、scikit-learn 和 Seaborn。
- `src/python_notes/tutorials/data_structures/advanced_structures.ipynb`: 数据结构和结构化工具补充，如 `bisect`、`OrderedDict`。
- `src/python_notes/tutorials/python_tools/stdlib_tools.ipynb`: Python 工具教程，包含 `math`、`cmath`、`decimal`、`fractions`、`calendar`、`sched` 和 APScheduler。
- `src/python_notes/tutorials/web_apps/gradio_streamlit.ipynb`: Gradio 和 Streamlit 教程，包含快速 Demo、组件组合、状态、缓存和运行方式。
- `src/python_notes/tutorials/web_automation/browser_automation_with_selenium.ipynb`: Selenium 浏览器自动化教程。
- `src/python_notes/tutorials/concurrency/concurrency.ipynb`: 并发编程教程，包含 threading、multiprocessing、asyncio、Ray、Dask 和任务队列对比。
- `src/python_notes/exercises/`: 配套练习、参考答案、测评资料和项目练习。
- `src/python_notes/resources/`: notebook 引用的图片、数据集和 PDF 参考资料。
- `src/python_notes/examples/task_queues/`: 任务队列可运行示例，包含 Celery、Dramatiq、ARQ。
