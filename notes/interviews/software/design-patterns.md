---
date created: 2024-03-19 17:22
date updated: 2026-05-08 23:53
---

# 设计模式面试笔记

#### 主要的设计模式

- 创建型模式，主要关注对象的创建过程，确保代码的灵活性和可重用性，有单例模式、工厂模式、抽象工厂模式、原型模式等
- 结构型模式，主要关注类和对象之间的组合，以形成更大的结构，有装饰器模式、代理模式等
- 行为型模式，关注对象之间的通信，有策略模式、观察者模式
- 单例模式，一个类只有一个实例

```python
from flask import Flask


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class FlaskApp(metaclass=SingletonMeta):
    def __init__(self):
        self.app = Flask(__name__)

    def run(self):
        self.app.run()


# 使用单例
app = FlaskApp()
app.run()
```

- 工厂模式，定义一个创建对象的接口，让子类决定实例化哪个类

```python
from flask import Flask


def create_app(config_name):
    app = Flask(__name__)

    # 根据配置名称加载不同的配置
    config_map = {
        "development": "config.DevelopmentConfig",
        "testing": "config.TestingConfig",
        "production": "config.ProductionConfig",
    }
    app.config.from_object(config_map[config_name])

    # 注册蓝图或其他应用组件
    from yourapplication.views import main_blueprint

    app.register_blueprint(main_blueprint)

    return app


# 创建应用实例
app = create_app("development")
```

- 抽象工厂模式，创建一系列相关或相互依赖的对象接口，无需指定它们具体的类
- 原型模式，用原型示例指定创建对象的种类，通过原型模式来复制这个配置对象，并根据需要修改复制的对象

```python
import copy
from flask import Flask


class Config:
    def __init__(self, environment):
        self.environment = environment
        self.database_uri = None
        self.secret_key = None

    def clone(self):
        return copy.deepcopy(self)


# 配置基类
base_config = Config("base")
base_config.database_uri = "sqlite:///default.db"
base_config.secret_key = "<secret-key>"

# 创建开发环境配置
development_config = base_config.clone()
development_config.environment = "development"
development_config.database_uri = "sqlite:///development.db"

# 创建测试环境配置
testing_config = base_config.clone()
testing_config.environment = "testing"
testing_config.database_uri = "sqlite:///testing.db"

# 创建生产环境配置
production_config = base_config.clone()
production_config.environment = "production"
production_config.database_uri = "sqlite:///production.db"

# 工厂函数，根据环境创建Flask应用
def create_app(config):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = config.database_uri
    return app


# 创建并运行Flask应用
if __name__ == "__main__":
    app = create_app(development_config)
    app.run()
```

- 装饰器模式，动态地给一个对象添加一些额外的职责

```python
from functools import wraps
from flask import Flask, redirect, url_for, session

app = Flask(__name__)

# 假设这是一个检查用户是否登录的装饰器
def login_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            # 如果用户未登录，重定向到登录页面
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def secret_page():
    return "This is a secret page!"


@app.route("/login")
def login():
    session["logged_in"] = True  # 假设登录逻辑
    return "You are logged in!"


if __name__ == "__main__":
    app.secret_key = "<secret-key>"
    app.run()
```

- 代理模式，为其他对象提供一种代理以控制对这个对象的访问，在 Flask 中不能直接实现代理模式，但可以通过中间件或蓝图来实现类似的功能

```python
from flask import Flask, Blueprint

# 创建一个蓝图对象，作为视图函数的代理
simple_page = Blueprint("simple_page", __name__)


@simple_page.route("/index")
def show_index():
    return "Index Page"


@simple_page.route("/about")
def show_about():
    return "About Page"


# 创建Flask应用并注册蓝图
app = Flask(__name__)
app.register_blueprint(simple_page)

if __name__ == "__main__":
    app.run()
```

- 策略模式，定义一系列的算法，并封装起来，并使它们可以互相替换

```python
from flask import Flask

app = Flask(__name__)

# 策略接口
class PaymentStrategy:
    def pay(self, order):
        raise NotImplementedError

# 具体策略A
class CreditCardStrategy(PaymentStrategy):
    def pay(self, order):
        return f"Paid {order.amount} using Credit Card"

# 具体策略B
class PayPalStrategy(PaymentStrategy):
    def pay(self, order):
        return f"Paid {order.amount} using PayPal"

# 上下文类
class Order:
    def __init__(self, amount):
        self.amount = amount
        self.payment_strategy = None

    def set_payment_strategy(self, strategy):
        self.payment_strategy = strategy

    def pay(self):
        if self.payment_strategy is None:
            raise ValueError("payment strategy is required")
        return self.payment_strategy.pay(self)


@app.route("/pay/<int:amount>/<string:method>")
def pay_order(amount, method):
    order = Order(amount)
    if method == "credit_card":
        order.set_payment_strategy(CreditCardStrategy())
    elif method == "paypal":
        order.set_payment_strategy(PayPalStrategy())
    else:
        return "Unknown payment method", 400
    return order.pay()


if __name__ == "__main__":
    app.run()
```

- 观察者模式，对象间的一对多依赖关系，当一个对象改变状态，依赖于它的对象都会被通知并自动更新

```python
from flask import Flask
from blinker import signal

app = Flask(__name__)

# 定义一个信号
user_updated = signal("user-updated")

# 定义一个观察者函数
def on_user_updated(sender, user):
    print(f"User {user['username']} has been updated.")


user_updated.connect(on_user_updated, app)


# 触发信号
def update_user(user):
    # 更新用户的逻辑
    print(f"Updating user {user['username']}...")
    # 触发信号
    user_updated.send(app, user=user)


@app.route("/update_user/<username>")
def update_user_route(username):
    user = {"username": username}
    update_user(user)
    return f"User {username} updated."


if __name__ == "__main__":
    app.run()
```
