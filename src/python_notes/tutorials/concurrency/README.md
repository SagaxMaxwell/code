# 并发模块

这个目录按并发领域和工具拆分 notebook。线程、进程、协程、任务队列和分布式计算各自独立成文件，便于单独学习和复习。

## threading

- [[event.ipynb|event]]: `threading.Event` 线程通知。
- [[condition.ipynb|condition]]: `threading.Condition` 条件变量和生产者消费者协作。
- [[locks.ipynb|locks]]: `threading.Lock`、`threading.RLock` 和锁使用规则。
- [[barrier.ipynb|barrier]]: `threading.Barrier` 阶段同步。
- [[semaphore.ipynb|semaphore]]: `threading.Semaphore` 和 `BoundedSemaphore` 并发限流。
- [[timer.ipynb|timer]]: `threading.Timer` 延迟执行。
- [[queue.ipynb|queue]]: `queue.Queue` 线程队列和队列类型对比。
- [[local.ipynb|local]]: `threading.local` 线程局部存储。

## multiprocessing

- [[pipe.ipynb|pipe]]: `multiprocessing.Pipe` 进程间管道通信。
- [[manager.ipynb|manager]]: `multiprocessing.Manager` 共享容器。
- [[pool.ipynb|pool]]: `multiprocessing.Pool` 进程池。
- [[memory.ipynb|memory]]: `Value`、`RawValue`、`Array` 和 `RawArray` 共享内存对象。
- [[simple_queue.ipynb|simple_queue]]: `multiprocessing.SimpleQueue` 进程间简单队列。

## concurrent.futures 和 asyncio

- [[executors.ipynb|executors]]: `ThreadPoolExecutor` 和 `ProcessPoolExecutor`。
- [[async.ipynb|async]]: `async`、`await`、`asyncio.run()` 和 `gather()`。
- [[tasks.ipynb|tasks]]: `create_task()`、任务调度和取消。
- [[taskgroup.ipynb|taskgroup]]: `asyncio.TaskGroup` 结构化并发。
- [[async_queue.ipynb|async_queue]]: `asyncio.Queue` 协程队列。

## 任务队列和分布式计算

- [[celery.ipynb|celery]]: Celery 后台任务和 Canvas 工作流。
- [[dramatiq.ipynb|dramatiq]]: Dramatiq actor、结果和 pipeline。
- [[arq.ipynb|arq]]: ARQ 异步任务队列。
- [[ray.ipynb|ray]]: Ray 远程函数和 Actor。
- [[dask.ipynb|dask]]: Dask 延迟任务图、本地集群和远程集群。
- [[comparison.ipynb|comparison]]: 进程、线程、协程以及任务工具选型对比。

任务队列的可运行代码示例放在 [[../../task_queues/README|task_queues]] 对应包目录中。
