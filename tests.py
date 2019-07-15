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


game = Sudoku()
times = []
for i in range(10):
    game.load_game(i)
    times.append(t.timeit(game.solve1, number=1))
    print(times[-1])

print(f'Average: {s.mean(times)}')