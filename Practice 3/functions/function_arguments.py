# 1
def print_name(fname):
    """function that receives parameter fname"""
    print(fname + " Refsnes")

print_name("Emil")
print_name("Tobias")
print_name("Linus")


# 2
def some_f(fname, lname):
    """function that receives 2 parameters"""  
    print(fname + " " + lname)
    
some_f("Emil", "Refsnes")


# 3
def defo(name = "friend"):
    """default value for parameter name"""
    print("Hello", name)

defo("Emil")
defo("Tobias")
defo()
defo("Linus")


# 4
def some_fruits(fruits):
    """parameter 'fruits' with data type list""" 
    for fruit in fruits:
        print(fruit)

my_fruits = ["apple", "banana", "cherry"]
some_fruits(my_fruits)


# 5
def func(a, b, /, *, c, d):
    """arguments before / are positional-only, and arguments after * are keyword-only"""
    return a + b + c + d

result = func(5, 10, c = 15, d = 20)
print(result)