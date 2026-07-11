---
date updated: 2026-07-10
---

# 量化模型

## 最小知识框架

量化模型不是先找复杂算法，而是先建立可验证闭环：

1. 数据：行情、成交、财务、另类数据。
2. 标签：未来收益、涨跌、波动率、回撤。
3. 特征：价格、成交量、技术指标、基本面、事件。
4. 模型：规则、线性模型、树模型、时序模型。
5. 回测：手续费、滑点、停牌、涨跌停、幸存者偏差。
6. 风控：仓位、止损、最大回撤、行业暴露。
7. 实盘：延迟、订单、监控、熔断。

## 收益率

```python
import pandas as pd

close = pd.Series([100, 102, 101, 105])
returns = close.pct_change()
future_return = close.shift(-1) / close - 1
```

建模时避免未来函数：任何特征只能使用当时已经知道的数据。

## 简单均线策略

```python
import pandas as pd


def moving_average_signal(close: pd.Series) -> pd.Series:
    fast = close.rolling(5).mean()
    slow = close.rolling(20).mean()
    return (fast > slow).astype(int)
```

这不是推荐策略，只是用来理解信号、持仓和收益计算。

## 机器学习建模

基本流程：

1. 按时间切分训练集、验证集、测试集，不能随机打乱。
2. 用过去窗口训练，用未来窗口验证。
3. 评估预测指标和交易指标，二者都要看。
4. 处理交易成本和容量。

常见指标：

- 年化收益
- 年化波动率
- 夏普比率
- 最大回撤
- 胜率和盈亏比
- 换手率

## 回测风险清单

- 幸存者偏差：只用当前仍存在的股票会高估收益。
- 前视偏差：用了未来才知道的数据。
- 手续费和滑点缺失。
- 调参过拟合。
- 忽略停牌、涨跌停和流动性。

## 学习建议

先用 pandas 实现最小回测器，再学习成熟框架。理解数据对齐、延迟和交易成本，比直接套模型更重要。

## 参考

- pandas 文档：<https://pandas.pydata.org/docs/>
- scikit-learn 文档：<https://scikit-learn.org/stable/>
