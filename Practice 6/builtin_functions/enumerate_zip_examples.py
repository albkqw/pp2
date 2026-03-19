names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]

# 1
for index, name in enumerate(names):
    print(index, name)

# 2
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# 3
value = "123"

if isinstance(value, str):
    converted = int(value)
    print("Converted to int:", converted)