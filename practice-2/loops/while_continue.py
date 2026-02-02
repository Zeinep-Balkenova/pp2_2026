i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    print(i)

i = 0
while i < 6:
    i += 1
    if i % 2 == 0:
        continue
    print(i)

numbers = [-1, 0, 1, 2]
i = 0
while i < len(numbers):
    if numbers[i] == 0:
        i += 1
        continue
    print(numbers[i])
    i += 1

x = 1
while x <= 4:
    if x == 2:
        x += 1
        continue
    print(x)
    x += 1

words = ["hi", "", "bye"]
i = 0
while i < len(words):
    if words[i] == "":
        i += 1
        continue
    print(words[i])
    i += 1

