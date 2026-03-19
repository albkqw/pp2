from functools import reduce

numbers = [1, 2, 3, 4, 5]

# 1
squared = list(map(lambda x: x**2, numbers))
print("Squared:", squared)

# 2
even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even)

# 3
sum_all = reduce(lambda x, y: x + y, numbers)
print("Sum:", sum_all)