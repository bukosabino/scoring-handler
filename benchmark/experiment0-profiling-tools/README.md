# Experiment

It is a first experiment to introduce the use of some modern tools to do profiling in Python.

It is not directly related with our project, but, I need some place to write pros and cons about these tools.

First, all our tools need to measure the time splitting by Python code, Native code (libraries written in C/C++) and System calls (e.g., `.sleep()`).

## How to run

```
pip install -r requirements.txt
```

## Scalene

To run:
```
scalene test_scalene.py
```

Output:
```
                                                                                          Memory usage: ▅▅▅▆▅▅▅▆▇▅▅▅ (max:  20.15MB)                                                                                          
                                                    /home/dpadial/projects/scoring-handler/profiling/experiment0tools/utils.py: % of time = 100.00% out of   7.64s.                                                     
       ╷       ╷        ╷     ╷       ╷      ╷              ╷       ╷                                                                                                                                                         
  Line │Time % │Time %  │Sys  │Mem %  │Net   │Memory usage  │Copy   │                                                                                                                                                         
       │Python │native  │%    │Python │(MB)  │over time / % │(MB/s) │/home/dpadial/projects/scoring-handler/profiling/experiment0tools/utils.py                                                                         
╺━━━━━━┿━━━━━━━┿━━━━━━━━┿━━━━━┿━━━━━━━┿━━━━━━┿━━━━━━━━━━━━━━┿━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸
     1 │       │        │     │       │      │              │       │import time                                                                                                                                              
     2 │       │        │     │       │      │              │       │                                                                                                                                                         
     3 │       │        │     │       │      │              │       │                                                                                                                                                         
     4 │       │        │     │       │      │              │       │def f1(n):                                                                                                                                               
     5 │       │        │     │       │      │              │       │    s = 0                                                                                                                                                
     6 │    8% │        │     │   51% │  982 │▃▃▃▃▃ 51%     │       │    for i in range(n):                                                                                                                                   
     7 │   25% │     1% │  0% │       │ -970 │▃▃▄▃▃▃▃▂      │       │        s += i                                                                                                                                           
     8 │       │        │     │       │      │              │       │    return s                                                                                                                                             
     9 │       │        │     │       │      │              │       │                                                                                                                                                         
    10 │       │        │     │       │      │              │       │                                                                                                                                                         
    11 │       │        │     │       │      │              │       │def f2(n):                                                                                                                                               
    12 │       │    46% │     │       │      │              │       │    return sum(range(n))                                                                                                                                 
    13 │       │        │     │       │      │              │       │                                                                                                                                                         
    14 │       │        │     │       │      │              │       │                                                                                                                                                         
    15 │       │        │     │       │      │              │       │def f3(t):                                                                                                                                               
    16 │   19% │        │ 19% │       │      │              │       │    time.sleep(t)                                                                                                                                        
    17 │       │        │     │       │      │              │       │    return t                                                                                                                                             
       ╵       ╵        ╵     ╵       ╵      ╵              ╵       ╵      
```

#### Pros

* Elegant output info
* Clear memory usage details

#### Cons

* Not available Python API. You need to profile all the file, and sometimes we are not interested in some parts of the script (e.g. slow import like `import sklearn`)
* Not clear output when we call asyncio calls
* Code smell / not use of good practices

More info: https://github.com/emeryberger/scalene

## Pyinstrument

To run:
```
python test_pyinstrument.py
```

Output:
```
  _     ._   __/__   _ _  _  _ _/_   Recorded: 18:01:30  Samples:  3
 /_//_/// /_\ / //_// / //_'/ //     Duration: 4.272     CPU time: 2.770
/   _/                      v3.3.0

Program: test_pyinstrument.py

4.272 <module>  test_pyinstrument.py:1
├─ 1.502 f3  utils.py:15
│  └─ 1.502 sleep  <built-in>:0
│        [2 frames hidden]  <built-in>
├─ 1.481 f2  utils.py:11
│  └─ 1.481 sum  <built-in>:0
│        [2 frames hidden]  <built-in>
└─ 1.289 f1  utils.py:4
```

#### Pros

* Python API. We can `start()` and `end()` the profiler at any point in the script. This is really helpful when we want profile the backend of a REST API.

#### Cons

* Not clear output when we call asyncio calls

More info: https://github.com/joerick/pyinstrument


## Yappi

To run:
```
python test_yappi.py 
```

Output:
```
Clock type: WALL
Ordered by: totaltime, desc

name                                  ncall  tsub      ttot      tavg      
..ng/experiment0tools/utils.py:15 f3  1      0.000012  1.501701  1.501701
..ng/experiment0tools/utils.py:11 f2  1      0.000012  1.339881  1.339881
..ing/experiment0tools/utils.py:4 f1  1      1.202866  1.202866  1.202866
```

#### Pros

* Python API. We can `start()` and `end()` the profiler at any point in the script. This is really helpful when we want profile the backend of a REST API.
* Supports multithreaded, asyncio and gevent profiling.

#### Cons

* Vague output for system calls and native code.

More info: https://github.com/sumerc/yappi/


# Conclusions

We will use the 3 tools in the next experiments.