# 1
num2 = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, num2)) # removes the odd nums
print(odd_numbers)


# 2
numbers = [5, 12, 8, 20, 3]
result = list(filter(lambda x: x > 10, numbers)) # keeps numbers greater than 10
print(result)  


# 3
words = ["cat", "elephant", "dog", "giraffe"]
result = list(filter(lambda x: len(x) > 3, words)) # keeps words with length greater than 3
print(result)  


# 4
people = [("Emil", 20), ("Anna", 16), ("John", 18)]
result = list(filter(lambda x: x[1] >= 18, people)) # keeps people who are 18 or older
print(result)  
