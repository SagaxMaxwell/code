from work import add

# 异步发送任务到 Dramatiq
add.send(3, 5)
