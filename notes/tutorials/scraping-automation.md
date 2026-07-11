---
date updated: 2026-07-10
---

# 爬虫与网页自动化

## 选择工具

| 工具 | 适合场景 |
| --- | --- |
| `httpx` + 解析库 | 静态页面、API、简单抓取 |
| Scrapy | 大规模抓取、调度、去重、管道 |
| Playwright | 现代浏览器自动化、E2E、动态页面 |
| Selenium | 仍可用于传统浏览器自动化或已有项目维护 |

优先判断页面数据是否来自接口。能直接请求接口就不要开浏览器；只有 JS 渲染、登录态复杂或需要真实用户行为时才使用 Playwright/Selenium。

## Scrapy 核心对象

- Spider：定义入口 URL、解析逻辑和后续请求。
- Selector：用 CSS/XPath 取数据。
- Item / dataclass：结构化数据。
- Pipeline：清洗、去重、保存。
- Middleware：代理、UA、重试、限速。

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css(".quote"):
            yield {
                "text": quote.css(".text::text").get(),
                "author": quote.css(".author::text").get(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

## Playwright

Playwright 自动等待元素可用，定位优先使用用户可感知语义。

```python
from playwright.sync_api import expect, sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    expect(page.get_by_role("heading")).to_be_visible()
    browser.close()
```

定位优先级：

1. `get_by_role`
2. `get_by_label`
3. `get_by_text`
4. `get_by_test_id`
5. CSS/XPath

## Selenium

Selenium 仍然有价值，尤其是企业已有自动化项目。新项目若没有历史包袱，E2E 通常优先评估 Playwright。

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")
heading = driver.find_element(By.TAG_NAME, "h1")
print(heading.text)
driver.quit()
```

## 合规与稳定性

- 遵守网站条款、robots 协议和访问频率限制。
- 对登录态、验证码、个人数据保持谨慎，不绕过访问控制。
- 抓取任务必须有重试、超时、限速、断点续跑和日志。
- 数据保存前做 schema 校验，避免脏数据进入后续流程。

## 参考

- Scrapy 官方文档：<https://docs.scrapy.org/en/latest/>
- Playwright Python 文档：<https://playwright.dev/python/docs/intro>
- Selenium 官方文档：<https://www.selenium.dev/documentation/>

