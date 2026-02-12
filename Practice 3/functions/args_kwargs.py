# 1
def func(*kids):
    """takes value from tuple of values"""
    print("The youngest child is " + kids[2])
func("Emil", "Tobias", "Linus")


# 2
def some_f(*args):
    """shows what *args is"""
    print("Type:", type(args))
    print("First argument:", args[0])
    print("Second argument:", args[1])
    print("All arguments:", args)
some_f("Emil", "Tobias", "Linus")


# 3
def my_function(greeting, *names):
    for name in names:
        print(greeting, name)

# here "Hello" is assigned to greeting, and the rest are collected in names
my_function("Hello", "Emil", "Tobias", "Linus")


# 4
def suma(*numbers):
    """returns the sum of nums"""
    total = 0
    for num in numbers:
        total += num
    return total

print(suma(1, 2, 3))
print(suma(10, 20, 30, 40))
print(suma(5))


# 5
def wow(**myvar):
    """it shows what **kwargs is"""
    print("Type:", type(myvar))
    print("Name:", myvar["name"])
    print("Age:", myvar["age"])
    print("All data:", myvar)

wow(name = "Tobias", age = 30, city = "Bergen")


# 6
def what(username, **details):
    """receives 1 positional argument and **kwargs argument""" 
    print("Username:", username)
    print("Additional details:")
    for key, value in details.items():
        print(" ", key + ":", value)

what("emil123", age = 25, city = "Oslo", hobby = "coding")