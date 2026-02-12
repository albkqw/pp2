# 1
class A:
    def hello(self):
        print("Hello from A")


class B:
    def hi(self):
        print("Hi from B")


class C(A, B):
    pass


c = C()
c.hello()
c.hi()


# 2
class Fly:
    def move(self):
        print("Flying")


class Walk:
    def move(self):
        print("Walking")


class Bird(Fly, Walk):
    pass


Bird().move()  # method resolution order


# 3
class A:
    x = 1


class B:
    x = 2


class C(A, B):
    pass


print(C.x)


# 4
class Parent1:
    def show(self):
        print("Parent1")


class Parent2:
    def show(self):
        print("Parent2")


class Child(Parent1, Parent2):
    pass


Child().show()
