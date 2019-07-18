# SudokuSolver
A Sudoku solver and generator

## How to use
```
python SudokuSolver.py [-n GRID_NUMBER] [-f FILENAME]
```
The games.txt provides an exemple of how the file must be.

or

The following code reads a file containing the games, solves the selected one and prints on the screen:

```python
from SudokuSolver import *

game = Sudoku()
game.open(1, "games.txt")
game.solve()

print(game)
```

The grid number and the file name are optional. By default, it picks the first grid in the "games.txt" file

### Generate a sudoku board
just do:

```python
from SudokuSolver import *

game = Sudoku()
game.generate()

print(game)
```

You can pass a seed as argument to generate() or leave it blank for a random seed
