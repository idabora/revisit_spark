"""
1. Default Argument
2. Keyword Argument
3. Positional Argument
4. Arbitary Argument
5. Nested Functions / Closures
6. Anonymous function / lambda
7. Pass by Refernece & Pass by Value
"""


"""
1. Default Argument
"""


def default_argument(firstname="Anurodh", lastname="kumar"):
    print(firstname, lastname)


# default_argument()
# default_argument(firstname="hello")
# default_argument(lastname="hello")
# default_argument("hello", "good morning")


"""
2. Keyword Argument
"""


def args_kwargs(*args, **kwargs):
    print(args)
    args[3] = "arpit" 
    # my_name = "arpit"
    print(args)
    print(kwargs)
    for a in kwargs.values():
        print(a)


# args_kwargs("my", "name", "is", "anurodh", greeting="Good Morning", time="11:11")

"""
5. Nested Functions / Closures
"""

def closure():
    counter = 0

    def increment():
        nonlocal counter
        counter += 1
        return counter

    return increment


# one = closure()
# print(one())
# print(one())
# print(one())
# print(one())

"""
6. Anonymous function / lambda
"""

f = lambda arg: arg*arg
print(f(10))

result = lambda x: "POSITIVE" if x > 0 else "NEGATIVE" if x < 0 else "ZERO"
print(result(4))

my_func = [lambda res=i:res for i in range(1, 10)]

for i in my_func:
    print(i())


res = [lambda arg=i: arg*arg for i in range(1, 11)]
for i in res:
    print(i())

res = [num for num in range(1, 11) if num % 2 == 0 ]
print(res)

res = map(lambda x: x*x, [i for i in range(1, 11)])
print(list(res))

ress = filter(lambda x: x>10 and x<15,  [i for i in range(1, 21)])
print(list(ress))

from functools import reduce

res = reduce(lambda x, y: x+y, [i for i in range(1, 6)])
print(res)