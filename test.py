import multiprocessing
import time


def producer(q):
    for i in range(5):
        time.sleep(1)
        print(f"Producer putting item {i} into queue")
        q.put(i)  # 向队列中放入数据


def consumer(q):
    for _ in range(5):
        item = q.get()  # 从队列中取出数据
        print(f"Consumer got item {item} from queue")
        time.sleep(2)  # 模拟处理时间


if __name__ == "__main__":
    # 创建一个 SimpleQueue 对象
    q = multiprocessing.SimpleQueue()

    # 创建并启动生产者进程和消费者进程
    producer_process = multiprocessing.Process(target=producer, args=(q,))
    consumer_process = multiprocessing.Process(target=consumer, args=(q,))

    producer_process.start()
    consumer_process.start()

    producer_process.join()  # 等待生产者进程完成
    consumer_process.join()  # 等待消费者进程完成
