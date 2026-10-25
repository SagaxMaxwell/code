# Learning

按主题组织的知识笔记、可运行实验和练习。

- `.md`：适合阅读、检索和长期维护的知识
- `.ipynb`：需要运行并观察结果的实验
- `.py`：仅用于自动检查，或必须被其他程序导入的实现

## 主题

- [[python/README|Python]]
- [[algorithms/README|算法与练习]]
- [[data/README|数据与数据库]]
- [[testing/README|测试与汽车诊断]]
- [[web/README|Web 开发与自动化]]
- [[systems/README|系统与网络]]
- [[engineering/README|软件工程]]
- [[roadmap|学习路线]]

同一主题的笔记与实验放在同一目录；没有运行需求时，不创建 Notebook。

```bash
ruff check .
python -m unittest discover -s tests
```
