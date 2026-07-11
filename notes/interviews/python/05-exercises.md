---
date created: 2024-07-01 13:13
date updated: 2026-05-08 23:53
---

# Python Coding Exercises

#### `numpy` 数组相对于嵌套的 Python 列表有哪些优势？

- 列表不支持向量化操作，列表必须存储每个元素的类型信息，在操作时必须执行类型调度代码
- `numpy` 高效且方便，可进行向量与矩阵运算
- 数组和列表具有相同的数据存储方式
- 数组只能保存单个数据类型元素，而列表可以保存任何数据类型元素

#### 代码运行结果

```python
def multiplexers():
    return [lambda n: index * n for index in range(4)]

print([m(2) for m in multiplexers()])
# [6, 6, 6, 6]
```

#### Python 为什么没有重载？

- 是解释型语言，函数重载现象通常出现在编译型语言中
- 其次 Python 是动态类型语言，函数的参数没有类型约束，也就无法根据参数类型来区分重载
- 再者 Python 中函数的参数可以有默认值，可以使用可变参数和关键字参数，因此即便没有函数重载，也要可以让一个函数根据调用者传入的参数产生不同的行为

#### 输入年月日，判断这个日期是这一年的第几天?

```python
import datetime

def which_day(year, month, day):
    end = datetime.date(year, month, day)
    start = datetime.date(year, 1, 1)
    return (end - start).days + 1
```

#### 逆波兰表达式（后缀表达式）？

```python
import operator


def eval_rpn(tokens):
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": lambda a, b: int(a / b),
    }
    stack = []

    for token in tokens:
        if token in operators:
            if len(stack) < 2:
                raise ValueError("invalid RPN expression")
            b = stack.pop()
            a = stack.pop()

            if token == "/" and b == 0:
                raise ZeroDivisionError("division by zero")

            stack.append(operators[token](a, b))
        else:
            stack.append(int(token))

    if len(stack) != 1:
        raise ValueError("invalid RPN expression")

    return stack[0]


print(eval_rpn(["3", "4", "+", "2", "*", "7", "/"]))
# 2
```

#### 运行结果？

```python
def extend_list(val, items=[]):
    items.append(val)
    return items

list1 = extend_list(10)
list2 = extend_list(123, [])
list3 = extend_list('a')
print(list1)
print(list2)
print(list3)
```

```ascii
[10, 'a']
[123]
[10, 'a']
```

#### 运行下面的代码是否会报错，如果报错请说明哪里有什么样的错，如果不报错请说出代码的执行结果？

```python
class A: 
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

obj = A(1)
obj.__value = 2
print(obj.value)
print(obj.__value)
```

```ascii
1
2
```

> 打印 `obj. Value` 时，它返回的是通过 `@property` 装饰器定义的原始私有属性 `__value` 的值，而打印 `obj.__value` 时，它返回的是新创建的属性 `__value` 的值，即 2
> 添加 `__slots__ = ('__value', )` 则可以禁止代码运行时动态的给对象添加新属性
> `@property` 装饰器将属性转换为只读属性

#### 检测列表深度？

```python
def list_depth(value):
    if not isinstance(value, list):
        return 0

    return 1 + max((list_depth(item) for item in value), default=0)


print(list_depth([[1], [2, [3]]]))
# 3
```

#### 有一个通过网络获取数据的函数（可能会因为网络原因出现异常），写一个装饰器让这个函数在出现指定异常时可以重试指定的次数，并在每次重试之前随机延迟一段时间，最长延迟时间可以通过参数进行控制？

```python
from functools import wraps
from random import uniform
from time import sleep


def retry(*, retry_times=3, max_wait_secs=5, errors=(Exception,)):
    if retry_times < 1:
        raise ValueError("retry_times must be at least 1")

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retry_times + 1):
                try:
                    return func(*args, **kwargs)
                except errors:
                    if attempt == retry_times:
                        raise
                    sleep(uniform(0, max_wait_secs))

        return wrapper

    return decorate
```

#### 实现字符串反转的代表性方法？

```python
def reverse_by_slice(content):
    return content[::-1]


def reverse_by_reversed(content):
    return "".join(reversed(content))


def reverse_in_place(content):
    content_len = len(content)
    chars = list(content)

    for index in range(content_len // 2):
        opposite = content_len - index - 1
        chars[index], chars[opposite] = chars[opposite], chars[index]

    return "".join(chars)
```
