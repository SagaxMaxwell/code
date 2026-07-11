---
date created: 2024-07-01 13:13
date updated: 2026-05-08 23:53
---

# Python 其他问题

#### 正则表达式的 `match ()` 方法和 `search ()` 方法有什么区别？

- 使用正则表达式有两种方式，一种是直接调用 `re` 模块中的函数，传入正则表达式和需要处理的字符串；一种是先通过 `re` 模块的 `compile ()` 函数创建正则表达式对象，然后再通过对象调用方法并传入需要处理的字符串
- 如果一个正则表达式被频繁的使用，推荐用 `re.compile()` 函数创建正则表达式对象，这样会减少频繁编译同一个正则表达式所造成的开销
- `match ()` 方法是从字符串的起始位置进行正则表达式匹配，返回 `Match` 对象或 `None`，`search ()` 方法会扫描整个字符串来找寻匹配的模式，同样也是返回 `Match` 对象或 `None`
- 其他方法有
	- `findall ()`，查找所有匹配项
	- `sub ()`，替换文本
	- `split ()`，分割文本

#### `namedtuple ()` 的用法和作用？

- 只有属性没有方法的类
- 命名元组与普通元组一样是不可变容器
- 和普通元组不同的是，命名元组中的数据有访问名称，可以通过名称而不是索引来获取保存的数据，不仅在操作上更加简单，代码的可读性也会更好

```python
from collections import namedtuple

Card = namedtuple("Card", ("suit", "rank"))

card1 = Card("红桃", 13)
card2 = Card("梅花", 5)

print(f"{card1.suit}{card1.rank}")
print(f"{card2.suit}{card2.rank}")
```

- 命名元组的本质就是一个类，所以它还可以作为父类创建子类
- 命名元组内置了一系列的方法，例如，可以通过 `_asdict()` 方法将命名元组处理成字典，也可以通过 `_replace()` 方法创建命名元组对象的浅拷贝

```python
class MyCard(Card):
    def show(self):
        ranks = ["", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        return f"{self.suit}{ranks[self.rank]}"


print(Card)                         # <class '__main__.Card'>
card3 = MyCard("方块", 12)
print(card3.show())                 # 方块Q
print(card1._asdict())              # {'suit': '红桃', 'rank': 13}
print(card2._replace(suit="方块"))   # Card(suit='方块', rank=5)
```
