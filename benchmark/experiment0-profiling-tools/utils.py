import time


def f1(n):
    s = 0
    for i in range(n):
        s += i
    return s


def f2(n):
    return sum(range(n))


def f3(t):
    time.sleep(t)
    return t
