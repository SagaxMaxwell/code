import asyncio


# 生产者协程
async def producer(queue):
    for i in range(5):
        print(f"Producer: producing {i}")
        await queue.put(i)  # 将数据放入队列
        await asyncio.sleep(1)


# 消费者协程
async def consumer(queue):
    while True:
        item = await queue.get()  # 从队列中取出数据
        if item is None:  # 如果是 None，说明生产者已结束，退出消费者
            break
        print(f"Consumer: consumed {item}")
        queue.task_done()  # 标记任务完成
        await asyncio.sleep(2)


async def main():
    # 创建一个容量为 3 的队列
    queue = asyncio.Queue(maxsize=3)

    # 创建生产者和消费者任务
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    # 等待生产者完成
    await producer_task
    # 向消费者发送停止信号（None）
    await queue.put(None)
    # 等待消费者完成
    await consumer_task


# 启动事件循环并执行 main 协程
asyncio.run(main())
