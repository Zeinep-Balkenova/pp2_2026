class A:
    def init(self):
        print("A")

class B(A):
    def init(self):
        super().init()

class Parent:
    def greet(self):
        print("Hi")

class Child(Parent):
    def greet(self):
        super().greet()

class Shape:
    def area(self):
        return 0

class Square(Shape):
    def area(self):
        return super().area()

class Base:
    def init(self, x):
        self.x = x
