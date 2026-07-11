---
date created: 2024-03-19 17:22
date updated: 2026-05-08 23:53
---

# 工具、部署与 Selenium 笔记

#### Docker

| 特性      | 描述                                            |
| ------- | --------------------------------------------- |
| 容器化技术   | 将应用程序及其依赖打包成可移植的容器                            |
| 轻量级     | 启动速度快，资源消耗低                                   |
| 可扩展性    | 轻松扩展，处理更多负载                                   |
| 隔离性     | 容器之间相互独立，易于部署和管理                              |
| 一致性     | 提供一个一致的运行环境，无论在哪个环境中的应用都相同                    |
| 自动化     | 支持自动化部署和构建，使用 Dockerfile 和 Docker Compose 等工具 |
| 社区和生态系统 | 拥有大量预构建镜像和工具，支持多种编程语言和框架                      |

#### Docker 使用场景

| 场景     | 描述                           |
| ------ | ---------------------------- |
| 开发环境一致 | 创建一致的开发环境，减少部署问题             |
| CI/CD  | 集成 CI/CD 工具，自动构建、测试和部署应用程序   |
| 微服务    | 封装微服务，独立部署和扩展，便于团队协作和系统维护    |
| 自动化测试  | 快速创建测试环境，进行自动化测试             |
| 云计算    | 在云环境中部署和管理容器化应用程序            |
| 数据科学   | 创建数据科学工作流程容器，便于重复实验          |
| Serverless器   | 集成Serverless器架构，运行特定任务的代码           |
| 数据库和存储 | 部署和管理数据库和存储服务                |
| 网络和安全  | 构建安全的网络隔离环境，用于开发、测试和部署网络相关应用 |

#### Static

| 修饰的元素 | 作用                                                  | 场景                                                |
| ----- | --------------------------------------------------- | ------------------------------------------------- |
| 类成员变量 | 成为类级别的变量，所有实例共享，直接通过类名访问，程序生命周期内始终存在                | 常量（如 `Math. PI`）、工具类中的变量（如长度单位）                   |
| 类方法   | 成为类级别的，不需创建对象即可调用，不能直接访问非静态变量和方法，可以访问静态变量，可以有返回值和参数 | 工具类中的方法（如 `Math. Max (int a, int b)`）、初始化单例模式中的实例 |
| 代码块   | 在类加载时执行，用于初始化静态变量，可以有返回值和参数                         | 初始化静态变量                                           |

> 静态变量和静态方法在类加载时被创建，并且随着类的消失而消失
> 静态变量和静态方法可以被类的所有实例共享，因此如果多个实例修改了同一个静态变量，可能会导致不可预知的结果
> 静态变量和静态方法可以直接通过类名访问，而无需创建类的实例
> 静态变量和静态方法不能直接访问非静态变量和非静态方法，但可以通过创建类的实例来间接访问

#### Nginx 和 uwsgi

| 组件    | 类型              | 性能            | 用途                                |
| ----- | --------------- | ------------- | --------------------------------- |
| nginx | HTTP 的反向代理服务器   | 高并发处理能力和低内存消耗 | 常用于静态内容服务、负载均衡和代理服务器              |
| uWSGI | Web 服务器和应用程序服务器 | 高效的多线程和多进程模型  | 常用于部署 Python 应用程序，也可以与其他语言的框架一起使用 |

#### `Model` 对象的主键如何定义自增、uuid 的生成策略、雪花算法

- 自增主键
	- `db. Column (db. Integer, primary_key=True, autoincrement=True)` 来定义一个自增主键
- UUID
	- 用 `db. Column (db. String (36), primary_key=True, unique=True, default=lambda id: uuid.uuid4().hex)` 来定义一个 UUID 主键
	- UUID 是一种全局唯一的标识符，通常由系统生成，可以确保每个主键都是唯一的
- 雪花算法
	- Snowflake 是一种分布式 ID 生成算法，用于生成全局唯一 ID
	- Snowflake 算法生成的 ID 由多个部分组成，包括时间戳、机器 ID、数据中心 ID 和序列号，这些部分组合起来生成一个 `64` 位的整数

#### Selenium 的启动细节，启动配置，元素定位方法，在页面执行 JavaScript 脚本，标签切换

- 启动细节
	- 启动 Driver
	- Chrome 创建 Session 时打开了浏览器与 Selenium 无关，是 ChromeDriver 的功劳
- 启动配置

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()

# 无头模式
options.add_argument("--headless=new")

# 隐形模式
options.add_argument("--incognito")

# window.navigator.webdriver
options.add_argument("--disable-blink-features=AutomationControlled")

# User-Agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# 启动
driver = webdriver.Chrome(options=options)
```

- 元素定位方法

```python
from selenium.webdriver.common.by import By

driver.find_element(By.ID, "username")
driver.find_element(By.NAME, "username")
driver.find_element(By.CLASS_NAME, "form-control")
driver.find_element(By.TAG_NAME, "input")
driver.find_element(By.LINK_TEXT, "登录")
driver.find_element(By.PARTIAL_LINK_TEXT, "登")
driver.find_element(By.XPATH, "//input[@name='username']")
driver.find_element(By.CSS_SELECTOR, "input[name='username']")
```

> Selenium 4 推荐使用 `find_element(By.*, value)`，旧的 `find_element_by_*()` 系列 API 已废弃。

- 执行 JavaScript 脚本

```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
```

- 标签切换

```python
# 切换到新标签页
driver.switch_to.window(driver.window_handles[-1])

# 切换到 iframe
driver.switch_to.frame(0)

# 切换到默认内容
driver.switch_to.default_content()
```

#### Selenium 隐藏机器人身份

- 修改 `WebDriver` 属性

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
```

- 使用 IP 代理还有 User-Agent

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


proxy = "12.34.56.78:9000"
options = Options()
options.add_argument(f"--proxy-server=http://{proxy}")

driver = webdriver.Chrome(options=options)
```

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
driver = webdriver.Chrome(options=options)
```

- 隐形模式

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--incognito")  # 隐形模式

extension_path = "path/to/extension.crx"  # 扩展文件路径
options.add_extension(extension_path)
driver = webdriver.Chrome(options=options)
```

- 限速爬取
