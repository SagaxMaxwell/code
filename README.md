# Python 项目

教程、练习、资源和任务队列示例。

- `src/learnpy/`：可安装包、教程与练习
- `../notes/`：独立的系统、数据库、面试和实践笔记

维护约定：一个主题对应一个 notebook；可运行代码放在包目录，静态文件放在 `assets/`。

```bash
ruff check src tests
python -m unittest discover
```
