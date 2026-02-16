def total(*args):
    print(sum(args))
total(1, 2, 3)

def show(*args):
    print(args)
show("a", "b", "c")

def user(**kwargs):
    print(kwargs)
user(name="Alex", age=19)

def mix(a, *args):
    print(a, args)
mix(1, 2, 3)

def full(**data):
    for k, v in data.items():
        print(k, v)
