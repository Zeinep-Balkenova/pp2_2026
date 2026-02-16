class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class Animal:
    def sound(self):
        print("Sound")

class Dog(Animal):
    def sound(self):
        print("Bark")

class Parent:
    def work(self):
        print("Work")

class Child(Parent):
    def work(self):
        print("Study")
