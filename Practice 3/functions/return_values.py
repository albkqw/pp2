# 1
def add(a, b):
    """returns the sum of two numbers"""
    return a + b  

# 2
def is_even(n):
    """checks if number is even"""
    return n % 2 == 0   

# 3
def square(x):
    """returns square of the number"""
    return x * x   

# 4
def max_value(a, b):
    """returns bigger value"""
    if a > b:
        return a  
    return b      

# 5
def string_length(text):
    """returns string length"""
    return len(text)  


print(add(3, 5))
print(is_even(10))
print(square(4))
print(max_value(7, 9))
print(string_length("Python"))
