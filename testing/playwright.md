---
date updated: 2026-07-26
---

# Playwright

## Playwright 教程

### 适合场景

Playwright 是现代浏览器自动化工具，适合 E2E 测试、跨浏览器验证、动态页面抓取、登录流程验证和关键用户路径回归测试。它能驱动 Chromium、Firefox、WebKit，并且默认带自动等待机制。

优先用 Playwright 做真实浏览器行为验证。静态页面或直接暴露数据接口的场景，优先使用 `httpx`、Scrapy 或接口测试，避免为简单抓取启动浏览器。

### 安装

使用 pytest 插件：

```bash
uv add --dev pytest-playwright
uv run playwright install
```

只安装 Chromium：

```bash
uv run playwright install chromium
```

运行测试：

```bash
uv run pytest
uv run pytest --browser chromium --headed
uv run pytest --browser chromium --browser firefox
```

### 第一个测试

`pytest-playwright` 会提供 `page`、`browser`、`context` 等 fixture。

```python
from playwright.sync_api import Page, expect


def test_example_domain(page: Page) -> None:
    page.goto("https://example.com")

    expect(page.get_by_role("heading", name="Example Domain")).to_be_visible()
    expect(page.get_by_role("link", name="More information")).to_have_attribute(
        "href",
        "https://www.iana.org/domains/example",
    )
```

Playwright 会自动等待元素出现、可见、可点击或断言成立。测试里少写 `sleep()`，优先使用 locator 和 `expect()`。

### Locator 优先级

定位要尽量接近用户看到和操作的语义。

| 优先级 | 写法 | 适合场景 |
| --- | --- | --- |
| 1 | `get_by_role()` | 按按钮、链接、标题、输入框等可访问角色定位 |
| 2 | `get_by_label()` | 表单字段 |
| 3 | `get_by_placeholder()` | 输入框占位文本稳定时 |
| 4 | `get_by_text()` | 稳定文案 |
| 5 | `get_by_test_id()` | 产品文案容易变化时 |
| 6 | `locator("css")` | 兜底，不建议作为首选 |

```python
page.get_by_role("button", name="Login").click()
page.get_by_label("Email").fill("alice@example.com")
page.get_by_test_id("submit-order").click()
expect(page.get_by_text("Order created")).to_be_visible()
```

稳定的 E2E 测试依赖稳定 locator。CSS 类名和 DOM 层级经常因为样式重构变化，不适合做核心定位。

### 录制与调试

录制用户操作：

```bash
uv run playwright codegen https://example.com
```

带界面运行：

```bash
uv run pytest --headed --slowmo 300
```

开启调试：

```bash
PWDEBUG=1 uv run pytest -k login --headed
```

失败排查常用参数：

```bash
uv run pytest --screenshot only-on-failure --video retain-on-failure --tracing retain-on-failure
```

`codegen` 适合生成起点，不适合直接把录制代码当最终测试。录制完成后要整理为清晰的步骤、稳定的 locator 和明确断言。

### Page Object

页面流程复杂时，用 Page Object 封装页面操作，让测试函数只表达业务路径。

```python
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        self.page.goto("https://example.com/login")

    def login(self, email: str, password: str) -> None:
        self.page.get_by_label("Email").fill(email)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Login").click()

    def expect_logged_in(self) -> None:
        expect(self.page.get_by_role("heading", name="Dashboard")).to_be_visible()


def test_login(page: Page) -> None:
    login_page = LoginPage(page)

    login_page.open()
    login_page.login("alice@example.com", "secret")
    login_page.expect_logged_in()
```

Page Object 不要写成万能工具类。一个类对应一个页面或一个稳定流程即可。

### 登录状态复用

反复登录会拖慢测试，也会让用例依赖登录页稳定性。可以先保存登录状态，再在后续上下文里复用。

```python
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/login")
    page.get_by_label("Email").fill("alice@example.com")
    page.get_by_label("Password").fill("secret")
    page.get_by_role("button", name="Login").click()
    page.context.storage_state(path="state.json")
    browser.close()
```

```python
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.goto("https://example.com/dashboard")
    browser.close()
```

项目里通常会把 `storage_state` 接入 pytest 配置或自定义 fixture。敏感账号和 token 不要提交到仓库。

### 网络控制

Playwright 可以等待请求、拦截接口、模拟响应，适合把前端流程和后端不稳定因素隔离开。

```python
from playwright.sync_api import Page, expect


def test_empty_recommendations(page: Page) -> None:
    page.route(
        "**/api/recommendations",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"items": []}',
        ),
    )

    page.goto("https://example.com")
    expect(page.get_by_text("No recommendations")).to_be_visible()
```

不要把所有接口都 mock 掉。E2E 的价值在于覆盖真实集成路径；mock 更适合隔离少量不稳定或昂贵依赖。

### 动态页面抓取

抓取动态页面时的基本流程：

```python
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    titles = page.get_by_role("heading").all_inner_texts()
    browser.close()

print(titles)
```

抓取项目必须加：

- 超时和重试。
- 限速和并发上限。
- 断点续跑。
- 数据 schema 校验。
- 对网站条款、robots 和个人数据边界的检查。

### 稳定性清单

- 每个测试只验证一个关键业务路径。
- 优先用 role、label、text、test id，少用 CSS/XPath。
- 每个流程至少有一个能证明结果的断言。
- 对跳转、弹窗、下载、上传、网络请求分别写明确等待。
- 测试数据要可重复创建和清理。
- CI 中保存失败截图、视频和 trace。
- E2E 用例数量控制在关键路径，更多规则放单元测试和 API 测试。

### 参考

- Playwright Python Intro：<https://playwright.dev/python/docs/intro>
- Playwright Locators：<https://playwright.dev/python/docs/locators>
- Playwright Assertions：<https://playwright.dev/python/docs/test-assertions>
- Playwright Codegen：<https://playwright.dev/python/docs/codegen>
