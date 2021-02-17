import yappi

from utils import f1, f2, f3

if __name__ == "__main__":
    yappi.set_clock_type("WALL")
    yappi.start()
    f1(25_000_000)
    f2(75_000_000)
    f3(1.5)
    yappi.get_func_stats().print_all()
