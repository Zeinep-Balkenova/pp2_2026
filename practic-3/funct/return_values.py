def add(a, b):
    return a + b
result = add(2, 3)

def square(x):
    return x * x
print(square(5))

def is_even(n):
    return n % 2 == 0

def stats(a, b):
    return a + b, a - b

s, d = stats(5, 2)

def nothing():
    return
