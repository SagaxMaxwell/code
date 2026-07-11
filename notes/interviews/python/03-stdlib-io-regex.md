---
date created: 2024-07-01 13:13
date updated: 2026-05-08 23:53
---

# Python Standard Library Io And Regex

#### Python 中与文件相关的库有哪些？

- `os`、`os.path` 和 `shutil`
- `os` 和 `os.path`，模块包含访问文件系统的功能
- `shutil`，模块使能够复制和删除文件

```python
import os
import shutil

source = "path/to/source.txt"
destination = "path/to/target.txt"
directory_path = "path/to/directory"
file_path = "path/to/file.txt"

# 复制文件
shutil.copy(source, destination)

# 删除整个目录
shutil.rmtree(directory_path)

# 删除文件
os.remove(file_path)
```

#### 如何用 Python 语言发送电子邮件？

- Python 提供了 `smtplib` 和 `email` 模块，将这些模块导入到创建的邮件脚本中，并通过对用户进行身份验证来发送邮件
- 它有一个方法 `SMTP (smtp-server, port)`，它需要两个参数来建立 SMTP 连接

```python
import smtplib
from email.message import EmailMessage


sender = "your_email@example.com"
receiver = "receiver_email@example.com"
smtp_server = "smtp.example.com"
username = "your_email_username"
password = "your_email_password"

msg = EmailMessage()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = "Test Email"
msg.set_content("This is a test email sent by Python.")

with smtplib.SMTP(smtp_server, 587) as server:
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
```

<!-- 兼容旧版写法 -->

```python
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 邮件发送者
sender = 'your_email@example.com'
# 邮件接收者
receiver = 'receiver_email@example.com'
smtp_server = 'smtp.example.com'
# 发送者邮箱的用户名和密码
username = 'your_email_username'
password = 'your_email_password'

# 邮件主题和内容
subject = 'Test Email'
content = 'This is a test email sent by Python.'

# 创建 MIMEText 对象
msg = MIMEText(content, 'plain', 'utf-8')
msg['From'] = Header(sender, 'utf-8')
msg['To'] = Header(receiver, 'utf-8')
msg['Subject'] = Header(subject, 'utf-8')

with smtplib.SMTP(smtp_server, 587) as server:
    server.starttls()
    server.login(username, password)
    server.sendmail(sender, receiver, msg.as_string())
```

#### 如何在 Python 中生成随机数？

- 使用随机模块 `random`

```python
import random

mu = 0
sigma = 1

print(random.random())              # [0, 1) float
print(random.uniform(1, 3))          # [1, 3] float
print(random.randrange(1, 3))        # [1, 3) int
print(random.randint(1, 3))          # [1, 3] int
print(random.normalvariate(mu, sigma))  # 正态分布的浮点数
```

```ascii
0.34713710269387843
1.586492196951702
2
1
-0.34508903504989326
```

$$
\sigma = \sqrt{\frac{\sum{(x_i - \mu)^2}}{N}}​​
$$

#### 如何使用 `random` 模块生成随机数、实现随机乱序和随机抽样？

- `random.shuffle(x)` 函数可以实现对序列 `x` 的原地随机乱序
- `random.choice(seq)` 函数可以从非空序列中取出一个随机元素
- `random.choices(population, weights=None, *, cum_weights=None, k=1)` 函数可以从总体中随机抽取（有放回抽样）出容量为 `k` 的样本并返回样本的列表，可以通过参数指定个体的权重，如果没有指定权重，个体被选中的概率均等
- `random.sample(population, k)` 函数可以从总体中随机抽取（无放回抽样）出容量为 `k` 的样本并返回样本的列表

> `random` 模块提供的函数除了生成均匀分布的随机数外，还可以生成其他分布的随机数，例如 `random.gauss(mu, sigma)` 函数可以生成高斯分布（正态分布）的随机数

#### PYTHONPATH 是什么？

- `PYTHONPATH` 是导入模块时使用的环境变量
- 每当导入一个模块时，还会查找 `PYTHONPATH` 以检查各个目录中是否存在导入的模块
- 解释器使用它来确定要加载哪个模块

#### Python 中的 pickling 和 unpickling 是什么？

- Python pickle 被定义为一个模块，它接受任何 Python 对象并将其转换为字符串表示。它使用 `dump` 函数将 Python 对象转储到一个文件中；这个过程被称为 `pickling`
- 从存储的字符串表示中检索原始的 Python 对象的过程被称为 `unpickling`

#### Python 中的模块是什么？

- 模块是包含 Python 代码的文件
- 此代码可以是函数、类、变量

#### Python 中常用的内置模块

- `os`
- `system`
- `random`
- `time`
- `JSON`
- `math`

#### Python 中常用第三方库

- `pandas`
- `numpy`
- `scipy`
- `redis`
- `celery`
- `selenium`
- `matplotlib`
- `faker`

> 企业会自己构建库

#### Python 中有哪些环境变量，有什么用？

- `PYTHONPATH`，与 PATH 变量相同，Python 解释器使用它来搜索模块文件
- `PYTHONHOME`，这是一个额外的 PATH 变量来搜索模块
- `PYTHONSTARTUP`，它存储包含 Python 代码的初始化脚本的路径，每次 Python 解释器启动时它都会运行
- `PYTHONCASEOK`，在 Windows 中，它使 Python 在 `import` 语句中找到第一个不区分大小写的匹配项，需要将其设置为激活

#### 如何在 Python 中将字符串转换/更改为 int 或 long ？

- Python 3 中只有 `int`，不再区分 `int` 和 `long`。
- `int(x, base=10)` 可将字符串按指定进制转换为整数，例如 `int("1010", 2)` 返回 `10`。
- 转换失败会抛出 `ValueError`，实际开发中要在用户输入场景做异常处理。

#### 如何在 Python 中创建套接字？

- 使用 `socket.socket()` 创建套接字，`AF_INET` 表示 IPv4，`SOCK_STREAM` 表示 TCP。

```python
import socket

simple_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

#### 在 Python 中为什么使用 `__init__.py` 模块？

- 它通过排除具有通用名称 (如字符串) 的目录，使 Python 将目录解释为包
- 它授予程序员控制权来决定哪个目录是包，哪个不是包
- 但是，`__init__.py` 也可以是一个空文件。然后它可以帮助执行包的初始化代码或设置 `__all__` 变量。

#### 如何在 Python 中运行带有参数的子进程或外部程序？

- `os`，`subprocess`，`threading`，`multiprocessing`
- `subprocess`，现代模块
	- `subprocess.call()`，运行命令，等待命令完成，并返回命令的退出状态码
	- `subprocess.run()`，运行命令，等待命令完成，并返回 `CompletedProcess` 对象
	- `subprocess.Popen()`，运行命令，并提供更多的控制和灵活性，如处理输入输出流和管道
- `os.system()`
- `os.popen()`
- `commands`，旧模块
- `pty`，伪终端
- `threading` 和 `multiprocessing`，如果你需要并行运行多个子进程，可以使用这些模块来创建线程或进程

#### Python 正则表达式语法

| 字符类      | 描述                                 |
| -------- | ---------------------------------- |
| `.`      | 匹配除换行符之外的任何 `1` 个字符                |
| `[abc]`  | 匹配方括号内的任意 `1` 个字符                  |
| `[^abc]` | 匹配不在方括号内的任意 `1` 个字符                |
| `\d`     | 匹配一个数字字符，等价于 `[0-9]`               |
| `\D`     | 匹配一个非数字字符，等价于 `[^0-9]`             |
| `\w`     | 匹配包括下划线的任何单词字符，等价于 `[A-Za-z 0-9_]` |
| `\W`     | 匹配任何非单词字符，等价于 `[^A-Za-z 0-9_]`     |
| `\s`     | 匹配任何空白字符，包括空格、制表符、换行符等等            |
| `\S`     | 匹配任何非空白字符                          |

| 量词       | 描述                     |
| -------- | ---------------------- |
| `*`      | 匹配前面的子表达式零次或多次         |
| `+`      | 匹配前面的子表达式一次或多次         |
| `?`      | 匹配前面的子表达式零次或一次         |
| `{n}`    | `n` 是一个非负整数，恰好匹配 `n` 次 |
| `{n,}`   | 至少匹配 `n` 次             |
| `{n, m}` | 至少匹配 `n` 次且最多匹配 `m` 次  |

| 定位符  | 描述                 |
| ---- | ------------------ |
| `^`  | 匹配输入字符串的开始位置       |
| `$`  | 匹配输入字符串的结束位置       |
| `\b` | 匹配一个单词边界，即字与空格间的位置 |
| `\B` | 非单词边界匹配            |

| 分组和引用     | 描述                             |
| --------- | ------------------------------ |
| `(exp)`   | 匹配 `exp` 并捕获文本到自动命名的组里         |
| `(?:exp)` | 匹配 `exp` 但不捕获匹配的文本             |
| `\n`      | `n` 是一个正整数，引用编号为 `n` 的捕获组匹配的文本 |

| 选择符  | 描述                   |
| ---- | -------------------- |
| `\|` | 匹配两个或多个分支选择的任意 `1` 个 |

| 反义符      | 描述         |
| -------- | ---------- |
| `[^...]` | 表示不在括号中的字符 |

| 断言         | 描述                        |
| ---------- | ------------------------- |
| `(?=exp)`  | 正向先行断言，匹配 `exp` 前面的位置     |
| `(?! Exp)` | 负向先行断言，匹配后面跟的不是 `exp` 的位置 |

#### 贪婪匹配与非贪婪匹配

| 贪婪量词     | 非贪婪量词     | 描述                                      |
| -------- | --------- | --------------------------------------- |
| `*`      | `*?`      | 匹配前面的元素零次或多次，非贪婪版本会尽可能少地匹配              |
| `+`      | `+?`      | 匹配前面的元素一次或多次，非贪婪版本会尽可能少地匹配              |
| `?`      | `??`      | 匹配前面的元素零次或一次，非贪婪版本会尽可能少地匹配              |
| `{m, n}` | `{m, n}?` | 匹配前面的元素至少 `m` 次但不超过 `n` 次，非贪婪版本会尽可能少地匹配 |

#### 使用 Python 代码实现遍历一个文件夹的操作？

- `os.walk(path)`
- `os.listdir(path)`
- `os.scandir(path)`，配合 `with`
- `pathlib.Path(path).iterdir()`

```python
from pathlib import Path

for path in Path("/Users/Hao/Downloads").rglob("*"):
    print(path)
```

```python
import os

for root, dir_names, file_names in os.walk("/Users/Hao/Downloads"):
    for dir_name in dir_names:
        print(os.path.join(root, dir_name))
    for file_name in file_names:
        print(os.path.join(root, file_name))
```

#### Python 中如何实现字符串替换操作？

- `re.compile().sub()`
- `str.replace()`

#### 如何读取大于内存的文件？

- 分片
- 分段读取
- 通过 `read ()` 方法的 `size` 参数指定读取的大小
- 通过 `seek ()` 方法的 `offset` 参数指定读取的位置

```python
chunk_size = 2 * 1024 * 1024

with open("large_file.bin", "rb") as file:
    for chunk in iter(lambda: file.read(chunk_size), b""):
        process(chunk)
```
