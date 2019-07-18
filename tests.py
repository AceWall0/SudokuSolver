import timeit as t
import statistics as s
from SudokuSolver import *

def f(i):
    x = i % 9
    y = i // 9
    return (x//3) + (y//3)*3

def g(i):
    x = i % 9
    y = i // 9
    return (x%3) + (y%3)*3

def testTime():
    # a = Sudoku()
    # times = []
    # for i in range(1, 21):
    #     a.open(i)
    #     times.append(t.timeit(a.solve1, number=1))
    #     print(i, '=', times[-1])
    #
    # print(f'Average: {s.mean(times)}\n')

    b = Sudoku()
    times = []
    for i in range(1, 51):
        b.open(i)
        times.append(t.timeit(b.solve, number=1))
        print(i, '=', times[-1])

    print(f'Average: {s.mean(times)}\n')



def testSudoku():
    a = Sudoku()
    a.open(1)
    a.solve()

    print()

    b = Sudoku()
    b.open(1)
    b.solve1()


if __name__ == '__main__':
    testTime()