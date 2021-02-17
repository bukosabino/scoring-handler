from pyinstrument import Profiler

from utils import f1, f2, f3

if __name__ == "__main__":
    profiler = Profiler()
    profiler.start()
    f1(25_000_000)
    f2(75_000_000)
    f3(1.5)
    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))
