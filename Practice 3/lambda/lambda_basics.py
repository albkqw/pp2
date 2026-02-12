# 1
x = lambda a : a + 10 # add 10 to argument a, and return the result
print(x(5))


# 2
y = lambda a, b, c : a + b + c # returns the sum of a,b,c
print(y(1,2,3))


# 3
def func(n):
    """function in the another function"""
    return lambda a: a * n

f = func(12)
print(f(20)) 


# 4
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))