---
date updated: 2026-07-10
---

# 汽车 UDS

## 基本概念

UDS（Unified Diagnostic Services）是汽车 ECU 诊断服务体系，常见于刷写、读故障码、读写数据标识、例程控制和安全访问。它通常跑在 CAN、CAN FD、DoIP 等传输之上。

学习顺序：

1. CAN 基础：帧 ID、数据长度、仲裁、波特率。
2. ISO-TP：把长诊断报文分片到 CAN 帧。
3. UDS 服务：请求 SID、响应 SID、NRC 负响应码。
4. 安全访问、会话控制、例程控制。
5. 刷写流程和日志分析。

## 常见服务

| SID | 服务 | 用途 |
| --- | --- | --- |
| `0x10` | DiagnosticSessionControl | 切换默认/扩展/编程会话 |
| `0x11` | ECUReset | ECU 重启 |
| `0x22` | ReadDataByIdentifier | 读取 DID |
| `0x2E` | WriteDataByIdentifier | 写 DID |
| `0x27` | SecurityAccess | 种子密钥安全访问 |
| `0x31` | RoutineControl | 启动/停止/查询例程 |
| `0x34` | RequestDownload | 请求下载刷写数据 |
| `0x36` | TransferData | 传输数据块 |
| `0x37` | RequestTransferExit | 结束传输 |
| `0x3E` | TesterPresent | 保持诊断会话 |

## Python 工具链

- `python-can`：CAN 总线访问。
- `can-isotp`：ISO-TP 传输。
- `udsoncan`：UDS 客户端。
- 厂商或项目内的 `libautomotive`：通常封装诊断脚本、刷写流程和日志工具，先看它对以上三层的抽象方式。

## 最小流程

```text
连接 CAN/DoIP
切换扩展会话 0x10
安全访问 0x27
读写 DID 0x22 / 0x2E
执行例程 0x31
发送 TesterPresent 保活
关闭连接
```

## 调试重点

- 请求和响应的 CAN ID 是否匹配。
- 是否需要功能寻址或物理寻址。
- 是否收到负响应 NRC，例如 `0x78` ResponsePending。
- 会话是否超时，是否需要周期性 `TesterPresent`。
- 安全访问算法和计数器是否被锁定。

## 参考

- udsoncan 文档：<https://udsoncan.readthedocs.io/en/latest/>
- python-can 文档：<https://python-can.readthedocs.io/en/stable/>

