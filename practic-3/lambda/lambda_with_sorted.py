nums = [3, 1, 2]
sorted(nums, key=lambda x: x)

words = ["apple", "kiwi"]
sorted(words, key=lambda x: len(x))

pairs = [(1, 3), (2, 1)]
sorted(pairs, key=lambda x: x[1])

names = ["Bob", "alex"]
sorted(names, key=lambda x: x.lower())

nums = [-1, 2, -3]
sorted(nums, key=lambda x: abs(x))
