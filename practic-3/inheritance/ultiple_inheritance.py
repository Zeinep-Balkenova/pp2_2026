class A:
    pass

class B:
    pass

class C(A, B):
    pass

class Fly:
    def move(self):
        print("Fly")

class Walk:
    def move(self):
        print("Walk")

class Human(Walk, Fly):
    pass

class X:
    x = 1
class Y:
    y = 2
class Z(X, Y):
    pass
