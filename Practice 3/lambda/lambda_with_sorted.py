# 1
students = [("Emil", 20), ("John", 22), ("Tim", 13)]
res = sorted(students, key=lambda x: x[1]) # sorts a list of tuples by the 2nd element
print(res)


# 2
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x)) # sorts strings by length
print(sorted_words)


# 3
numbers = [3, 15, 7, 20, 12, 1]
result = sorted(filter(lambda x: x > 10, numbers), reverse=True) # keeps numbers > 10 and sorts in descending order
print(result)  


# 4
people = [("Emil", 20), ("Anna", 16), ("John", 18), ("Kate", 25)]
result = sorted(
    filter(lambda x: x[1] >= 18, people),
    key=lambda x: x[1]
) # keeps adults and sorts them by age
print(result)  

