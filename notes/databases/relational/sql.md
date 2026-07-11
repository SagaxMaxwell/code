---
date created: 2024-07-17 13:49
date updated: 2026-05-08 23:53
---

# SQL 笔记

### 基本概念

#### 数据库术语

- 数据库，保存有组织的数据的容器
- 数据表，将特定类型数据的结构化清单
- 模式，数据库和表的分布及特性
- 行，表中的记录
- 列，表的字段
- 主键，唯一标识每一行的一列或一组列

#### 语法要点

- 要以 `;` 结尾
- 语句不区分大小写
- 语句的空格被忽略
- 支持三种注释

```sql
-- 注释1
-- 注释2
/* 注释3 */
```

#### DB、DBS、DBMS 区别

- DB，数据库
	- 保存有组织的数据的容器
- DBS，数据库系统
	- 包括 DB 和 DBMS
- DBMS，数据库管理系统
	- 软件系统，管理数据库
	- 负责数据库底层操作，如数据存储、数据检索、事务管理、并发控制

#### SQL 分类

- 数据定义语言，DDL，**定义数据库对象**
	- `CREATE`、`ALTER`、`DROP`
- 数据操纵语言，DML，**读写数据库**
	- `INSERT`、`UPDATE`、`DELETE`、`SELECT`
- 事务控制语言，TCL，**管理数据库中的事务**
	- `COMMIT`、`ROLLBACK`
- 数据控制语言，DCL，**控制用户的访问权限**
	- `GRANT`、`REVOKE`
	- `CONNECT`、`SELECT`、`INSERT`、`UPDATE`、`DELETE`、`EXECUTE`、`USAGE`、`REFERENCES`

#### CRUD

- 插入数据，`INSERT INTO`

```sql
## 插入一行
INSERT INTO user
VALUES (10, 'root', 'root', 'xxxx@163.com');

## 插入多行
INSERT INTO user
VALUES
  (10, 'root', 'root', 'xxxx@163.com'),
  (12, 'user1', 'user1', 'xxxx@163.com'),
  (18, 'user2', 'user2', 'xxxx@163.com');

## 插入行的一部分
INSERT INTO user(username, password, email)
VALUES ('admin', 'admin', 'xxxx@163.com');

## 插入查询出来的数据
INSERT INTO user(username)
SELECT name
FROM account;
```

- 读取数据，`SELECT`

```sql
SELECT prod_id, prod_name, prod_price
FROM products;

SELECT *
FROM products;

-- 查询不同的值
SELECT DISTINCT vend_id
FROM products;

-- 返回前 5 行
SELECT *
FROM mytable
LIMIT 5;

SELECT *
FROM mytable
LIMIT 0, 5;

-- 返回第 3 ~ 5 行
SELECT *
FROM mytable
LIMIT 2, 3;
```

- 更新数据，`UPDATE`

```sql
UPDATE user
SET username='robot', password='robot'
WHERE username = 'root';
```

- 删除数据，`DELETE`

```sql
DELETE FROM user
WHERE username = 'robot';

## 清空表的数据
TRUNCATE TABLE user;
```

#### `ORDER BY` 排序

- 对结果集按照一个列或一组列排序，默认升序
- 对多列排序时，先排序的列放前面，并且不同的列可以设置不同的排序规则

```sql
SELECT * FROM products
ORDER BY prod_price DESC, prod_name ASC;
```

#### `GROUP BY` 分组

- 可以按一列或多列分组
- 为每个组返回一个记录
- 将记录分组汇总到行中

```sql
SELECT cust_name, COUNT(cust_address) AS addr_num
FROM Customers
GROUP BY cust_name
ORDER BY cust_name DESC;
```

> `GROUP BY` 搭配 `ORDER BY` 使用时，必须先分组再排序
> 通常涉及聚合操作

#### `HAVING`

- 对汇总的 `GROUP BY` 分组结果进行过滤

> `WHERE`，过滤指定的行，在 `GROUP BY` 之前
> `HAVING`，过滤分组，在 `GROUP BY` 之后

#### 子查询

- 将查询的结果作为其他查询的数据来源

#### 运算符

| 运算符       | 描述                |
| --------- | ----------------- |
| `=`       | 等于                |
| `<>`      | 不等于，默写版本可被写成 `!=` |
| `>`       | 大于                |
| `<`       | 小于                |
| `>=`      | 大于等于              |
| `<=`      | 小于等于              |
| `BETWEEN` | 在某个范围内            |
| `LIKE`    | 搜索某种模式            |
| `IN`      | 指定针对某个列的多个可能值     |

```sql
SELECT * FROM Customers
WHERE cust_name = 'Kids Place';

UPDATE Customers
SET cust_name = 'Jack Jones'
WHERE cust_name = 'Kids Place';

DELETE FROM Customers
WHERE cust_name = 'Kids Place';
```

> 上述运算符可在 `WHERE` 后使用
> `WHERE` 用于过滤记录
> `WHERE` 后跟着返回 `TRUE` 或 `FALSE` 的条件

#### `IN` 和 `BETWEEN`

- `IN`，在几个特定的值中任选一个值
- `BETWEEN`，选取某个范围的值

#### `AND`、`OR`、`NOT`

- 略

#### `LIKE`

- 用于匹配文本
- 支持 `%` 和 `_` 通配符
	- `%`，表示字符出现任意次数
	- `_`，表示字符出现一次

```sql
SELECT prod_id, prod_name, prod_price
FROM products
WHERE prod_name LIKE '%bean bag%';

SELECT prod_id, prod_name, prod_price
FROM products
WHERE prod_name LIKE '__ inch teddy bear';
```

#### 连接

- 将两张表或多张表按照某个字段联合，将字段值相同的记录合并，形成仅存在于本次查询的临时表

```sql
SELECT c.cust_name, o.order_num
FROM Customers c
INNER JOIN Orders o
ON c.cust_id = o.cust_id
ORDER BY c.cust_name;

## USING
SELECT c.cust_name, o.order_num
FROM Customers c
INNER JOIN Orders o
USING(cust_id)
ORDER BY c.cust_name;
```

| 连接类型         | 说明                             |
| ------------ | ------------------------------ |
| `INNER JOIN` | 只有当两个表都存在满足条件的记录时才会返回行         |
| `LEFT JOIN`  | 返回左表中的所有行，右表不匹配的记录数据都置为 `NULL` |
| `RIGHT JOIN` | 返回右表中的所有行，左表不匹配的记录数据都置为 `NULL` |
| `FULL JOIN`  | 返回左右表的所有行，左右表不匹配的记录数据置为 `NULL` |
| `SELF JOIN`  | 将自身连接自身，至少需要重命名一个表             |
| `CROSS JOIN` | 交叉连接，从两个或者多个连接表中返回记录集的笛卡尔积     |

> 两张表的关联字段名相同，也可以使用 `USING` 子句来代替 `ON`
> `ON` 是表之间连接的条件，决定临时表的生成
> `WHERE` 是对临时表的数据进行过滤

#### 隐式内连接和显式内连接

```sql
## 隐式内连接
SELECT c.cust_name, o.order_num
FROM Customers c, Orders o
WHERE c.cust_id = o.cust_id
ORDER BY c.cust_name;

## 显式内连接
SELECT c.cust_name, o.order_num
FROM Customers c INNER JOIN Orders o
USING(cust_id)
ORDER BY c.cust_name;
```

> 使用 `WHERE` 实现隐式内连接
> 使用 `INNER JOIN` 实现显式内连接

#### `UNION`

- 将多个查询结果组合成结果集
- 所有查询的列数和列顺序必须相同
- 每个查询中涉及到表的列的数据类型必须兼容
- 通常返回的列名取自第一个查询

```sql
SELECT column_name(s) FROM table1
UNION ALL
SELECT column_name(s) FROM table2;
```

> `UNION ALL` 允许返回重复的值
> `UNION` 选取不同的值
> `UNION` 是垂直拼接，`JOIN` 是水平拼接
> `UNION` 连接的列必须相同，`JOIN` 连接的列允许不同

#### 其他关键字

- `DISTINCT`，去重
- `LIMIT`，显示返回的行数
- `ASC`，升序
- `DESC`，降序

#### 函数

- 文本处理

| 函数                  | 说明          |
| ------------------- | ----------- |
| `LEFT()`、`RIGHT()`  | 左边或者右边的字符   |
| `LOWER()`、`UPPER()` | 转换为小写或者大写   |
| `LTRIM()`、`RTRIM()` | 去除左边或者右边的空格 |
| `LENGTH()`          | 长度，以字节为单位   |
| `SOUNDEX()`         | 转换为语音值      |

```sql
SELECT *
FROM mytable
WHERE SOUNDEX(col1) = SOUNDEX('apple');
```

> **`SOUNDEX()`** 可以将一个字符串转换为描述其语音表示的字母数字模式

- 日期处理

| 函数              | 说明              |
| --------------- | --------------- |
| `AddDate()`     | 增加一个日期（天、周等）    |
| `AddTime()`     | 增加一个时间（时、分等）    |
| `CurDate()`     | 返回当前日期          |
| `CurTime()`     | 返回当前时间          |
| `Date()`        | 返回日期时间的日期部分     |
| `DateDiff()`    | 计算两个日期之差        |
| `Date_Add()`    | 高度灵活的日期运算函数     |
| `Date_Format()` | 返回一个格式化的日期或时间串  |
| `Day()`         | 返回一个日期的天数部分     |
| `DayOfWeek()`   | 对于一个日期，返回对应的星期几 |
| `Hour()`        | 返回一个时间的小时部分     |
| `Minute()`      | 返回一个时间的分钟部分     |
| `Month()`       | 返回一个日期的月份部分     |
| `Now()`         | 返回当前日期和时间       |
| `Second()`      | 返回一个时间的秒部分      |
| `Time()`        | 返回一个日期时间的时间部分   |
| `Year()`        | 返回一个日期的年份部分     |

> 日期格式，`YYYY-MM-DD`
> 时间格式，`HH:MM:SS`

- 数值处理

| 函数       | 说明  |
| -------- | --- |
| `SIN()`  | 正弦  |
| `COS()`  | 余弦  |
| `TAN()`  | 正切  |
| `ABS()`  | 绝对值 |
| `SQRT()` | 平方根 |
| `MOD()`  | 余数  |
| `EXP()`  | 指数  |
| `PI()`   | 圆周率 |
| `RAND()` | 随机数 |

- 汇总

| 函数        | 说明       |
| --------- | -------- |
| `AVG()`   | 返回某列的平均值 |
| `COUNT()` | 返回某列的行数  |
| `MAX()`   | 返回某列的最大值 |
| `MIN()`   | 返回某列的最小值 |
| `SUM()`   | 返回某列值之和  |

```sql
SELECT AVG(DISTINCT col1) AS avg_col
FROM mytable;
```

> `AVG()` 会忽略 `NULL`

#### 如何保证幂等性

- 幂等性指的是一个操作执行多次和执行一次的效果相同，即多次执行不会改变原有的状态
- `SELECT`、`DELETE`、`INSERT`（具有唯一性约束）、`UPDATE`（具有唯一性约束且不带触发器和级联更新）、数据库事务都是幂等的
- 确保幂等性
	- 使用唯一约束
	- 条件性更新
	- 使用幂等函数
	- 使用标识符

### 数据定义 DDL

#### 数据库操作

- 创建数据库

```sql
CREATE DATABASE test;
```

- 删除数据库

```sql
DROP DATABASE test;
```

- 选择数据库

```sql
USE test;
```

#### 数据表操作

- 创建表

```sql
CREATE TABLE user (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Id',
  username VARCHAR(64) NOT NULL DEFAULT 'default' COMMENT '用户名',
  password VARCHAR(64) NOT NULL DEFAULT 'default' COMMENT '密码',
  email VARCHAR(64) NOT NULL DEFAULT 'default' COMMENT '邮箱',
  PRIMARY KEY (id)
) COMMENT='用户表';

## 根据已有表创建新表
CREATE TABLE vip_user AS
SELECT * FROM user;
```

- 删除表

```sql
DROP TABLE user;
```

- 添加列

```sql
ALTER TABLE user
ADD age TINYINT UNSIGNED;
```

- 删除列

```sql
ALTER TABLE user
DROP COLUMN age;
```

- 修改列

```sql
ALTER TABLE user
MODIFY COLUMN age TINYINT UNSIGNED;
```

- 添加主键

```sql
ALTER TABLE user
ADD PRIMARY KEY (id);
```

- 删除主键

```sql
ALTER TABLE user
DROP PRIMARY KEY;
```

#### 视图操作

- 定义
	- 基于 SQL 语句的结果集的可视化的表
	- 不包含数据，不能进行索引操作，是虚拟表
- 作用
	- 简化 SQL 操作，如联结
	- 仅使用表的部分数据
	- 只给用户访问视图的权限，保证数据安全性
- 创建视图

```sql
CREATE VIEW top_10_user_view AS
SELECT id, username
FROM user
WHERE id < 10;
```

- 删除视图

```sql
DROP VIEW top_10_user_view;
```

#### 索引操作

- 用于快速查询和检索数据的数据结构
- 优点
	- 提高检索数据效率
	- 降低排序成本，建立索引默认会以升序排序
- 缺点
	- 索引创建和维护需要成本
	- 索引本身需要占用空间，数据量越多，占用空间就越多
	- DBMS 需要动态维护索引，会降低增删改的效率
- 创建索引

```sql
CREATE INDEX user_index
ON user (id);
```

- 创建唯一索引

```sql
CREATE UNIQUE INDEX user_index
ON user (id);
```

- 添加索引

```sql
ALTER TABLE user 
ADD INDEX user_index(id);
```

- 删除索引

```sql
ALTER TABLE user
DROP INDEX user_index;
```

#### 约束

- 约束表的数据规则和行为
- `NOT NULL`，不允许为 `NULL`
- `DEFAULT`，定义没有赋值时填充的默认值
- `CHECK`，保证列中的值符合指定的条件
- `UNIQUE`，保证每列的值都唯一
- `PRIMARY KEY`，确保某列有唯一标识符，是 `UNIQUE` 和 `NOT NULL` 的组合
- `FOREIGN KEY`，保证表中的数据匹配其他表的值，参照完整性

```sql
CREATE TABLE Users (
  Id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增Id',
  Username VARCHAR(64) NOT NULL UNIQUE DEFAULT 'default' COMMENT '用户名',
  Password VARCHAR(64) NOT NULL DEFAULT 'default' COMMENT '密码',
  Email VARCHAR(64) NOT NULL DEFAULT 'default' COMMENT '邮箱地址',
  Enabled TINYINT DEFAULT NULL COMMENT '是否有效',
  PRIMARY KEY (Id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

#### 完整性

- 实体完整性
	- 主键约束
- 参照完整性
	- 外键约束
- 用户定义完整性
	- 默认约束
	- 唯一约束
	- 检查约束
	- 非空约束
- 域完整性
	- 数据类型约束

### 事务处理 TCL

- `SELECT`、`CREATE`、`DROP` 不能回退
- MySQL 默认是隐式提交，每执行一条语句就当成一个事务进行提交，当出现 `START TRANSACTION` 语句时就会关闭隐式提交，当 `COMMIT` 或 `ROLLBACK` 语句执行后，事务会自动关闭，重新恢复隐式提交
- 通过 `SET AUTOCOMMIT=0` 可以取消自动提交，直到 `SET AUTOCOMMIT=1` 才会提交，`AUTOCOMMIT` 标记是针对每个连接而不是针对服务器的
- `START TRANSACTION`，指令用于标记事务的起始点
- `SAVEPOINT`，指令用于创建保留点
- `ROLLBACK TO`，指令用于回滚到指定的保留点；如果没有设置保留点，则回退到 `START TRANSACTION` 语句处
- `COMMIT`，提交事务

```sql
## 开始事务
START TRANSACTION;

## 插入操作 A
INSERT INTO `user`
VALUES (1, 'root1', 'root1', 'xxxx@163.com');

## 创建保留点 updateA
SAVEPOINT updateA;

## 插入操作 B
INSERT INTO `user`
VALUES (2, 'root2', 'root2', 'xxxx@163.com');

## 回滚到保留点 updateA
ROLLBACK TO updateA;

## 提交事务，只有操作 A 生效
COMMIT;
```

### 数据控制语言 DCL

#### `GRANT` 和 `REVOKE`

- `GRANT`，授予用户权限
- `REVOKE`，撤销用户权限
- `GRANT` 和 `REVOKE` 可在几个层次上控制访问权限
	- 整个服务器，使用 `GRANT ALL` 和 `REVOKE ALL`
	- 整个数据库，使用 `ON database.*`
	- 特定的表，使用 `ON database.table`
	- 特定的列
	- 特定的存储过程

```sql
GRANT privilege [, privilege] ...
ON privilege_level
TO user
[WITH GRANT OPTION];
```

> `GRANT` 关键字后指定一个或多个权限
> `ON privilege_level` 确定权限应用级别
> `user` 是要授予权限的用户，`GRANT` 语句将修改其权限，否则创建新用户
> `IDENTIFIED BY` 允许您为用户设置新的密码
> MySQL 支持全局 `*.*`、数据库 `database.*`、表 `database.table` 和列级别
> 可选 `WITH GRANT OPTION` 子句允许授予其他用户或从其他用户中删除拥有的权限

#### 创建账户

```sql
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
```

#### 修改账户名

```sql
RENAME USER 'myuser'@'localhost' TO 'newuser'@'localhost';
```

#### 删除账户

```sql
DROP USER 'myuser'@'localhost';
```

#### 查看权限

```sql
SHOW GRANTS FOR 'myuser'@'localhost';
```

#### 授予权限

```sql
GRANT SELECT, INSERT ON test.* TO 'myuser'@'localhost';
```

#### 删除权限

```sql
REVOKE SELECT, INSERT ON test.* FROM 'myuser'@'localhost';
```

#### 更改密码

```sql
ALTER USER 'myuser'@'localhost' IDENTIFIED BY 'mypass';
```

### 存储过程

#### 存储过程优缺点

- 优点
	- 代码封装，保证了一定的安全性
	- 代码复用
	- 由于是预先编译，因此具有很高的性能
- 缺点
	- 存储过程难以调试和扩展，更没有移植性

### 触发器

- 当触发器所在表出现指定事件时，将调用触发器对象
- 优点
	- SQL 触发器提供了另一种检查数据完整性的方法
	- SQL 触发器可以捕获数据库层中业务逻辑中的错误
	- SQL 不必等待运行计划任务，更改数据之前或之后会自动调用触发器
	- SQL 触发器对于审计表中数据的更改非常有用
- 缺点
	- SQL 触发器只能提供扩展验证，并且不能替换所有验证。必须在应用程序层中完成一些简单的验证
	- 从客户端应用程序调用和执行 SQL 触发器是不可见的，因此很难弄清楚数据库层中发生了什么
	- SQL 触发器可能会增加数据库服务器的开销
- 创建触发器

```sql
DELIMITER $
CREATE TRIGGER `trigger_insert_user`
AFTER INSERT ON `user`
FOR EACH ROW
BEGIN
  INSERT INTO `user_history`(user_id, operate_type, operate_time)
  VALUES (NEW.id, 'add a user', NOW());
END $
DELIMITER ;
```

- 查看触发器

```sql
SHOW TRIGGERS;
```

- 删除触发器

```sql
DROP TRIGGER IF EXISTS trigger_insert_user;
```

> MySQL 不允许在触发器中使用 `CALL` 语句，也就是不能调用存储过程

#### 触发器类型

- `BEFORE INSERT`，在将数据插入表格之前激活
- `AFTER INSERT`，将数据插入表格后激活
- `BEFORE UPDATE`，在更新表中的数据之前激活
- `AFTER UPDATE`，更新表中的数据后激活
- `BEFORE DELETE`，在从表中删除数据之前激活
- `AFTER DELETE`，从表中删除数据后激活

#### `NEW` 和 `OLD`

- MySQL 中定义了 `NEW` 和 `OLD` 关键字，用来表示触发器的所在表中，触发了触发器的那一行数据
- 在 `INSERT` 型触发器中，`NEW` 用来表示将要（`BEFORE`）或已经（`AFTER`）插入的新数据
- 在 `UPDATE` 型触发器中，`OLD` 用来表示将要或已经被修改的原数据，`NEW` 用来表示将要或已经修改为的新数据
- 在 `DELETE` 型触发器中，`OLD` 用来表示将要或已经被删除的原数据
