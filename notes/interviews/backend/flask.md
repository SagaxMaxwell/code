---
date created: 2024-07-29 11:55
date updated: 2026-05-08 23:53
---

# Flask 面试笔记

#### Flask 优势（为什么选择 Flask）

- 具有很小的 API，可以快速学习
- 符合 WSGI
- 具有内置的开发服务器
- 具有活跃的社区
- 具有大量的第三方扩展

#### 什么是 WSGI

- Python 中定义的 Web 服务器和 Web 应用程序之间或框架之间的通用接口标准
- WSGI 将 Web 组件分为 Web 服务器、Web 中间件、Web 应用程序
- WSGI 就是连接服务端（网关端）和应用端（框架端）的的桥梁，WSGI 的作用就是在协议之间进行转化
- 服务端接受 HTTP 请求，按照 WSGI 接口标准再调用注册的应用端，最后返回响应

#### Flask 的模板引擎

- 模板是包含静态、动态数据的文件
- 可在运行期间填充模板的动态数据，利用 Jinja 2 模板引擎使开发人员可以使用占位符的 HTML 模板创建动态数据
- 使用 `render_template()` 方法可以在运行时填充这些占位符

#### Flask 组件

- 路由和视图：把 URL 映射到处理函数，视图负责执行业务逻辑并返回响应。
- 请求和响应：`request` 读取参数、Header、Body；返回值会被 Flask 转成 `Response`。
- 上下文对象：`current_app`、`request`、`session`、`g` 基于上下文隔离当前应用和请求数据。
- 模板和静态文件：Jinja2 渲染 HTML，`static` 目录提供 CSS、JS、图片等资源。
- 扩展机制：通过 Flask-SQLAlchemy、Flask-WTF、Flask-Login 等扩展补充 ORM、表单、认证等能力。
- 错误处理和测试：支持自定义错误处理器、测试客户端和 CLI 命令。

#### Flask 生命周期

- WSGI 服务器接收 HTTP 请求并调用 Flask 应用。
- Flask 创建应用上下文和请求上下文，让 `request`、`session`、`g` 可用。
- 执行 `before_request`，匹配路由，调用视图函数。
- 视图返回字符串、字典、元组或 `Response`，Flask 统一转换为响应对象。
- 执行 `after_request` 和 `teardown_request`，发送响应并清理上下文。

#### Flask 定义路由

- 使用 Flask 实例创建
- 使用 BluePrint 实例创建

```python
# 动态路由
@app.route("/user/<username>", methods=["POST", "PATCH"])
def show_user_profile(username):
    # 使用字符串 "username" 访问 URL 中的动态部分
    return f"User: {username}"
```

#### Flask 中如何处理请求和响应

- 导入 Flask 模块
- 创建 Flask 实例
- 定义路由与视图函数
- 获取请求参数
- 构建响应
- 运行应用

#### Flask 中如何使用模板引擎

- 导入 `from flask import render_template`
- 配置模板目录，`app = Flask(__name__, template_folder="templates")`
- 定义路由与视图函数
- 创建模板文件，`templates` 目录下创建 HTML 文件
- 运行应用

#### Flask 中如何使用数据库

- `from flask_sqlalchemy import SQLAlchemy`
- 创建应用实例和配置数据库连接
- 定义模型类
- 初始化数据库
- 执行 CRUD
- 运行应用

#### Flask 如何使用蓝图

- `from flask import Blueprint`
- 创建蓝图实例
- 定义路由与视图函数
- 注册蓝图到应用
- 运行应用

#### Flask 如何处理静态文件

- 创建静态文件目录
- 配置静态文件路径，`app = Flask(__name__, static_folder="static")`
- HTML 文件引用静态文件
- 运行应用

#### Flask 如何处理错误和异常

- 使用 `try except`
- 定义错误处理器

```python
from flask import render_template


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500
```

- 自定义错误响应

```python
from werkzeug.exceptions import HTTPException


class CustomError(HTTPException):
    code = 400
    description = "Custom error message"

@app.errorhandler(CustomError)
def handle_custom_error(error):
    return render_template("custom_error.html", message=error.description), error.code
```

- 全局错误处理器

```python
@app.errorhandler(Exception)
def handle_unhandled_exception(e):
    return "An unexpected error occurred", 500
```

#### Flask 常用扩展

- `flask_sqlalchemy`
- `flask_redis`
- `flask_mail`
- `flask_jwt_extended`
- `flask_restful`
- `jinja2`
- `session`

#### 如何获取 Flask 的开发框架版本

- 使用 `git` 获取

```bash
git clone https://github.com/pallets/flask
cd flask && python3 setup.py develop
```

#### 如何安装 Flask

```bash
pip install flask
```

#### 如何创建 AJAX 应用程序

- 使用 Flask-Sijax（简单 AJAX）
- Flask-Sijax 是使用 Python/jQuery 的扩展
- 初始化并配置完成后，则支持 `@flask_sijax` 装饰器（装饰视图函数）

```python
import os
from flask import Flask, g, render_template
import flask_sijax

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app = Flask(__name__)

app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

@flask_sijax.route(app, '/hello')
def hello():
    def say_hi(obj_response):
        obj_response.alert('Hi there!')
    if g.sijax.is_sijax_request:
        g.sijax.register_callback('say_hi', say_hi)
        return g.sijax.process_request()
    return render_template('sijaxexample.html')
```

#### AJAX 是什么

- 用于创建交互式网页的技术
- 可在不重新加载整个页面的情况下与服务器交换数据和更新部分网页内容（局部更新）
- 浏览器与服务器进行异步数据交换，发送和接收数据不中断用户操作（异步通信）

#### Flask 默认主机地址和端口

- `127.0.0.1:5000`

> 主机地址就是 `localhost`

#### 如何修改主机地址和端口

- 修改 `run()` 方法的值传递

```python
# run 函数值传递
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

#### 如何在 Flask 获取请求参数

- 使用 `request` 对象和获取请求的参数

```python
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    val = request.args.get("var")
    return "Hello, World! {}".format(val)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

#### Flask 获取用户代理

```python
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    val = request.args.get("var")
    user_agent = request.headers.get("User-Agent")

    response = """
    <p>
        Hello, World! {}
        <br/>
        You are accessing this app with {}
    </p>
    """.format(val, user_agent)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

#### `url_for()` 函数作用

- `url_for()` 函数帮助创建动态路由

```python
from flask import Flask, url_for

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/user/<username>')
def profile(username):
    return f'Profile page for {username}'

with app.test_request_context():
    print(url_for('hello'))  # 输出: /hello
    print(url_for('profile', username='john'))  # 输出: /user/john
```

#### 视图函数怎么使用 `url_for()`

- 重定向

```python
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/view1')
def view1():
    # 这里可以执行一些操作，然后重定向到 view2
    return redirect(url_for('view2'))

@app.route('/view2')
def view2():
    return 'This is view2'

if __name__ == '__main__':
    app.run()
```

#### 如何在 Flask 创建管理界面

- 使用 Flask-Admin 扩展在 Flask 中创建一个管理界面
- 使用 Flask-Appbuilder 扩展，扩展已自带管理界面

#### 可以使用 Flask 创建哪种类型的应用程序

- 可以创建几乎所有类型的 Web 应用程序
- 单页应用程序、RESTful API 应用程序、SaaS 应用程序、中小型网站、静态网站、微服务、Serverless 应用等

> 单页应用程序，动态重写当前页面与用户的交互，避免了页面的重新加载 (单页应用程序框架有 React，Angular，Vue)
> 静态网页，静态网页是指不需要服务端处理、内容固定、不经常变化的网页
> SaaS 是 Software as a Service，指通过网络提供的软件服务，例如在线 CRM、协作文档、云后台等
> Serverless 应用程序，是云计算的执行模型，无需直接管理服务器，通常按事件触发和资源使用计费

#### 如何将 Twitter 或类似 API 与 Flask 应用程序集成

- 同时使用 Flask-Social 和 Flask-Security
- 可验证 Twitter、Facebook、Google 等账户
- 还需要通过在外部帐户提供商上注册 Flask 应用程序来获取使用者密钥和安全密钥

#### 为什么 Flask 被称为微框架

- 是因为 Flask 仅提供核心功能，例如请求、路由、Blueprint
- 对于其他功能，例如缓存，ORM，表单等需要使用其他的扩展

#### Flask 中的线程局部对象是什么意思

- Flask 中的 `request`、`session`、`g`、`current_app` 是上下文本地代理对象，本质上根据当前请求或应用上下文找到真实对象。
- 在多线程或协程环境中，不同请求访问到的是各自上下文中的对象，避免把请求对象手动层层传递。
- 使用这些对象时必须处于有效上下文中，否则会出现 “Working outside of request/application context” 之类的错误。

#### Flask 中的应用程序上下文是什么

- 是 Flask 中实现请求上下文（Request Context）和应用程序全局变量的基础
- 主要目的是让某些对象在整个应用程序中全局可访问，如 `current_app` 和 `g` 对象
- `<APP_NAME>.run()`（启动应用时），`with <APP_NAME>.app_context():`（显式推送）都会进入应用程序上下文

> 应用程序上下文是针对整个应用程序的，是全局的，并且在整个应用程序的生命周期内都是活跃的
> 请求上下文是针对单个 HTTP 请求的，是临时的，只在处理请求时活跃

#### 如何在 Flask 中创建一个 RESTful 应用程序

- Flask-API
- Flask-RESTful
- Flask-RESTX
- Connexion

#### 如何调试 Flask 应用程序

- Flask 内置开发服务器，而开发服务器具有调试模式
- 调用 `<APP_NAME>.run()` 方法时，可以设置 `debug=True`

> 在部署到生产环境前应禁用调试模式

#### Flask 命令

- 激活虚拟环境，再使用命令

```bash
# 查看版本
flask --version

# 查看环境
flask env

# 创建应用程序的密钥
flask secret

# 查看注册的路由
flask routes

# 启动开发服务器
flask run

# 测试应用程序
flask test

# 进入命令行
flask shell
```

> [Flask 官方文档](https://flask.palletsprojects.com)

#### Django 和 Flask（Flask 定义）

- Django
	- 是使用 Python 编程语言创建的 Web 开发框架
	- 有许多内置功能，如管理员后端和具有迁移功能的 ORM
	- 创建时间早，更加成熟
- Flask
	- 是使用 Python 编程语言创建的且开源的 Web 开发框架
	- 该框架基于 Jinja 2 模板引擎和 WSGI Web 应用程序库之上
	- 适用于快速开发，简单易学（API 少）
	- 适合不需要大型代码库的轻量级 Web 应用程序
		- 易于开发微服务和 Serverless 的应用程序

#### Flask 与 SQLite

- SQLite 是 Python 内置的数据库
- 在视图内部导入 SQLite 并编写 SQL 语句就可直接和数据库交互
- Flask 通常使用 Flask-SQLAlchemy 扩展

> ORM 详解 [[../../databases/relational/orm|ORM]]

#### 在 Flask 中使用 Session

- `from flask import session`

```python
# 在请求之间保存数据可以使用 session
from flask import Flask, session
app = Flask(__name__)
app.secret_key = "<secret-key>"

@app.route("/use_session")
def use_session():
    if "songs" not in session:
        session["songs"] = {"title": "Tapestry", "singer": "Bruno Major"}
    return session.get("songs")

@app.route("/delete_session")
def delete_session():
    session.pop("songs", None)
    return "removed song from session"
```

#### Flask 的 `g` 对象

- `g` 是请求/应用上下文中的临时命名空间，常用于保存当前请求期间复用的数据，如数据库连接、当前用户等。
- `g` 的生命周期通常随请求结束而结束，不适合跨请求保存数据。
- 跨请求状态应放在 Session、缓存、数据库或其他持久化存储中。

> 每个请求都有单独的 `g` 对象，实现了请求隔离和数据隔离

#### Flask 可以通过哪些方式连接数据库

- 使用 Flask-SQLAlchemy 扩展
- 对于 NoSQL 数据库，使用 Flask-MongoEngine (MongoDB)，Flask-Redis (Redis)

#### Flask 蓝图的作用

- 构建大型应用
- 优化项目结构
- 使功能模块化
- 增强可读性
- 易于维护

```python
from flask import Blueprint

book_bp = Blueprint("book", __name__)

@book_bp.route("/books")
def list_books():
    return "book list"

# 在应用工厂或 app 初始化处注册蓝图
from book import book_bp
app.register_blueprint(book_bp)
```

#### Flask 框架默认 Session 处理机制

- Flask 默认使用签名 Cookie 保存 Session 数据。
- 处理流程：序列化 Session 数据，使用 `SECRET_KEY` 签名防篡改，再编码后写入客户端 Cookie。
- 优点是无状态、部署简单，不需要服务端会话存储。
- 缺点是容量受 Cookie 限制，数据默认可被客户端读取，不能存敏感信息；`SECRET_KEY` 泄露会带来安全风险。
- 非永久 Session 通常随浏览器会话结束；永久 Session 的生命周期由 `PERMANENT_SESSION_LIFETIME` 控制。

#### Flask-WTF 是什么

- 适用于表单处理，数据校验并提供 CSRF 验证的功能扩展
- 能够使表单免受 CSRF（跨站请求伪造） 的攻击
- 可提供 `FileField` 处理文件上传，在表单提交后，自动从 `flask.request.files` 中抽取数据

```python
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.secret_key = "<secret-key>"  # 应从环境变量或密钥管理系统读取

# 定义表单类
class MyForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

# 定义路由和视图函数
@app.route("/", methods=["GET", "POST"])
def index():
    form = MyForm()
    if form.validate_on_submit():
        # 处理表单数据
        flash("收到来自 {} 的邮件地址 {}".format(form.name.data, form.email.data))
        return redirect(url_for("index"))
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
```

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask-WTF 表单示例</title>
</head>
<body>
    <h1>请填写以下表单</h1>
    <form method="post">
        {{ form.hidden_tag() }}
        <p>
            {{ form.name.label }}<br>
            {{ form.name(size=20) }}
        </p>
        <p>
            {{ form.email.label }}<br>
            {{ form.email(size=20) }}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
</body>
</html>
```

> `FileField.data` 属于 `Werkzeug` 对象

#### Flask 中添加邮件功能

```python
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# 配置邮件服务器信息
app.config["MAIL_SERVER"] = "smtp.example.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_email@example.com"
app.config["MAIL_PASSWORD"] = "your_password"

mail = Mail(app)

@app.route("/mail")
def email():
    msg = Message("Hello Message", sender="admin@test.com", recipients=["to@test.com"])
    mail.send(msg)
    return "Email sent!"

if __name__ == "__main__":
    app.run(debug=True)
```

#### 状态码

- `1xx`：信息响应，如 `100 Continue`。
- `2xx`：成功，如 `200 OK`、`201 Created`、`204 No Content`。
- `3xx`：重定向，如 `301 Moved Permanently`、`302 Found`、`304 Not Modified`。
- `4xx`：客户端错误，如 `400 Bad Request`、`401 Unauthorized`、`403 Forbidden`、`404 Not Found`。
- `5xx`：服务端错误，如 `500 Internal Server Error`、`502 Bad Gateway`、`503 Service Unavailable`。

#### DBUtils 模块的作用

- 实现数据库连接池
- 为了提高在多线程场景请求较多时的性能

#### Flask-SQLAlchemy 设置索引

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    __table_args__ = (
        db.Index("ix_user_email", "email"),
        db.UniqueConstraint("username", "email", name="uq_user_username_email"),
    )
```

> 在字段中设置 `index=True` 自动添加索引
> 在 `__table_args__` 可手动设置其他索引，参数为元组

#### Flask 如何配置到 Nginx 中

- 略
