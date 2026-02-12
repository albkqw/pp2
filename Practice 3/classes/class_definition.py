# 1
class MyClass:
    # This class with property x
    x = 5

o = MyClass()
print(o.x)


# 2
class Person:
    # This class represents a person
    pass
p1 = Person()


# 3
class Student:
    # Stores student information
    def __init__(self, name, age):
        self.name = name    
        self.age = age      

s1 = Student('Alibek', 18)
print(s1.name)
print(s1.age)


# 4
class Calculator:
    # Simple calculator class
    def add(self, a, b):
        return a + b

c1 = Calculator()
print(c1.add(2, 3))
