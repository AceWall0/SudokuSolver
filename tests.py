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
    #     a.open_game(i)
    #     times.append(t.timeit(a.solve1, number=1))
    #     print(i, '=', times[-1])
    #
    # print(f'Average: {s.mean(times)}\n')

    b = Sudoku()
    times = []
    for i in range(1, 51):
        b.open_game(i)
        times.append(t.timeit(b.solve2, number=1))
        print(i, '=', times[-1])

    print(f'Average: {s.mean(times)}\n')



def testSudoku():
    a = Sudoku()
    a.open_game(1)
    a.solve2()

    print()

    b = Sudoku()
    b.open_game(1)
    b.solve1()


if __name__ == '__main__':
    testTime()