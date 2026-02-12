# 1
class Person:
    def __init__(self, name):
        # Initializes person's name
        self.name = name
p1 = Person("Alibek")
print(p1.name)


# 2
class Student:
    def __init__(self, name, age):
        # Initializes student data
        self.name = name
        self.age = age
s1 = Student("Ivan", 15)
print(s1.name, s1.age)


# 3
class Car:
    def __init__(self, brand="Unknown"):
        # Sets car brand
        self.brand = brand
car = Car("Toyota")
print(car.brand)


# 4
class Rectangle:
    def __init__(self, width, height):
        # Initializes rectangle dimensions
        self.width = width
        self.height = height
r = Rectangle(20, 40)
print(f"width: {r.width}, height: {r.height}")


# 5
class User:
    def __init__(self, active):
        # Stores user status
        self.active = active

u = User(False)
print(f"user is active: {u.active}")