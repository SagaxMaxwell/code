---
date updated: 2026-07-10
---

# 学习路线

这份路线由原待办清单整理而来，重复项已合并，过时项已降级或删除。

## 优先级

1. 测试与 pytest：先补测试理论，再学 pytest 命令行参数、fixture、hook、插件和覆盖率。
2. Web 与自动化：FastAPI、Gradio、Scrapy、Playwright、Selenium 的定位和适用边界。
3. Python 工具链：typing、contextlib、队列、datetime、文件解析、Pydantic v2、msgspec。
4. 网络服务：socket、httpx、Nginx/Caddy、Consul、Paramiko、psutil。
5. 工程流程：CI/CD、E2E 自动化、DevOps、瀑布/敏捷、AI 工作流编排。
6. 专项扩展：UDS/汽车诊断、量化模型。

## 教程入口

- [[tutorials/testing-pytest|测试与 pytest]]
- [[tutorials/python-core|Python 核心补缺]]
- [[tutorials/validation-serialization|校验与序列化]]
- [[tutorials/web-api-apps|Web API 与应用]]
- [[tutorials/scraping-automation|爬虫与网页自动化]]
- [[tutorials/networking-services|网络服务]]
- [[tutorials/devops-workflow|DevOps 与工作流]]
- [[tutorials/automotive-uds|汽车 UDS]]
- [[tutorials/quant-models|量化模型]]

## 不再单独学习的旧项

- `pytest-pep8`：不作为新项目选择，统一使用 Ruff 做格式与 lint，再用 pytest 跑测试。
- 旧版 Python 兼容题：已从面试笔记中删除，现代 Python 只保留当前主流语义。
- CentOS 作为默认服务器首选：改为长期维护发行版优先。
