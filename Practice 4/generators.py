# 1
def gena_nums(n):
    for i in range(n):
        yield i*i

nums = gena_nums(5)
for i in nums:
    print(i)


# 2
n = int(input("Input n: "))
def gen_even(n):
    for i in range(n+1):
        if i%2 == 0:
            yield i
even = gen_even(n)
res = ','.join(str(num) for num in even)
print(res)


# 3
def divisible(n):
    for i in range(n+1):
        if (i%3 == 0) and (i%4 == 0):
            yield i
div = divisible(40)
for i in div:
    print(i)


# 4
def squares(a, b):
    for i in range(a, b+1):
        yield i**2
sq = squares(1, 10)
for i in sq:
    print(i)


# 5
def down(n):
    for i in range(n, -1, -1):
        yield i
d = down(10)
for i in d:
    print(i)