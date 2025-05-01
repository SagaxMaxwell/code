from work import add

result = add.apply_async((4, 6))
print("Task ID:", result.id)
print("Result:", result.get())
