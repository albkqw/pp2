# 1
class Animal:
    def sound(self):
        print("Some sound")


class Dog(Animal):
    def sound(self):
        print("Bark")


Dog().sound()


# 2
class Shape:
    def area(self):
        return 0


class Rectangle(Shape):
    def area(self):
        return 10


print(Rectangle().area())


# 3
class Parent:
    def show(self):
        print("Parent")


class Child(Parent):
    def show(self):
        print("Child")


Child().show()


# 4
class A:
    def greet(self):
        print("Hello")


class B(A):
    def greet(self):
        print("Hi")


B().greet()
