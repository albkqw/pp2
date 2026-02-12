# 1
def my_function():
    """prints text"""
    print("Hello from a function")
my_function()


# 2
def fahrenheit_to_celsius(fahrenheit):
    """translates fahrenheit to celsius"""
    return (fahrenheit - 32) * 5 / 9
print(fahrenheit_to_celsius(77))


# 3
def just():
    """function that does not nothing and returns None"""
    pass

print(just())

# 4
def calc(a, b):
    """just the sum of 2 numbers"""
    return a+b
print(calc(2, 3))
