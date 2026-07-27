def add(*args):
    sum = 0
    for n in args:
        sum = sum + n
    return sum

print(add(1, 2, 3, 4, 5))

def calculator(n, **kwargs):
    # print(kwargs)
    # for key, value in kwargs.items():
    #     print(key)
    #     print(value)
    # print(kwargs["add"])
    n += kwargs["add"]
    n *= kwargs["multiply"]
    return n

print(calculator(2, add=3, multiply=5))