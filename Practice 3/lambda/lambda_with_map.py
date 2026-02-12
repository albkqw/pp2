# 1
num1 = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, num1)) # returns the double values
print(doubled)


# 2
nums = [2, 3, 4, 5]
squares = map(lambda x: x ** 2, nums)  # square each number
print(list(squares))


# 3
names = ["alice", "bob", "tim"]
upper_names = map(lambda x: x.upper(), names)  # convert to uppercase
print(list(upper_names))


# 4
students = [("Emil", 20), ("John", 22), ("Tim", 13)]
ages = map(lambda x: x[1], students)  # get age from tuple
print(list(ages))
