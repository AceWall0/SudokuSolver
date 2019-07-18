from random import choice, seed
import argparse


class CellList(list):
    """
    A list that when the "in" operator is called, looks for the item in the .value property of the elements in the list,
    as oppose to looking for the elements of the list
    """

    def __contains__(self, item):
        for obj in self:
            if obj and item == obj.value:
                return True


class Cell:
    fixed = False
    row: CellList
    column: CellList
    block: CellList
    _id = 0

    def __init__(self, v=0):
        self.value = v
        self.memory = []
        self._id = Cell._id
        Cell._id += 1

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Cell(value={self.value}, id={self._id})"


class Sudoku:
    def solve1(self):
        """Can be used to solve, but is mainly used to generate games. For solving, use solve() method. It is about
        33x faster, up to more than 500x times faster"""
        i = 0
        direction = 1
        while i < 81:
            cell = self.cells[i]
            if cell.fixed:
                i += direction
                continue

            available = self.__filter_options(cell)
            if available:
                val  = choice(available)
                cell.value = val
                cell.memory.append(val)
                direction = 1

            else:
                cell.value = 0
                cell.memory = []
                direction = -1

            i += direction


    def solve(self):
        """
        Solves the game previously builded.
        This solution tries to minimize the number of backtracking by putting the values in the cells with the smaller
        values available
        """

        k = 0
        steps = []          # keep track of wich 'k' values was made a modification
        guesses = []        # what 'k' values the algorithm made a guess
        guess_thr = 1       # minimal number of options to start guessing
        last_ind = -1       # the last index where a value was changed
        completed = False   # has the code been completed?

        while not completed:
            completed = True

            while True:
                i = k % 81

                # has made a entire loop without changing a value
                if i == last_ind:
                    guess_thr += 1


                cell = self.cells[i]
                if cell.value == 0:
                    completed = False  # there is still values to fill

                    available = self.__filter_options(cell)
                    if 0 < len(available) <= guess_thr:
                        val = available[0]
                        cell.value = val
                        cell.memory.append(val)
                        steps.append(k)
                        last_ind = i

                        # A guess was made
                        if guess_thr > 1:
                            guesses.append(k)
                            guess_thr -= 1


                    # There is no more option to the cell, so it should revert everything till
                    # the last k where a guess was made
                    elif len(available) == 0:
                        last_k = guesses.pop()
                        while k >= last_k:
                            i = k % 81
                            cell = self.cells[i]
                            cell.value = 0

                            if k == last_k: break

                            cell.memory = []
                            last_ind = i
                            k = steps.pop()
                        continue
                k += 1
                if i == 80: break

            if last_ind == -1:
                if guess_thr == 9:
                    raise RuntimeError("No solution for this game.")
                guess_thr += 1


    def generate(self, game_seed=None):
        """Builds a new game with all the cells filled"""
        seed(game_seed)
        self._build()
        self.solve1()


    def __filter_options(self, c):
        """What values can the cell 'c' have?"""
        options = tuple(range(1, 10))
        output = tuple(x for x in options if x not in c.memory)
        output = tuple(x for x in output if x not in c.row)
        output = tuple(x for x in output if x not in c.column)
        output = tuple(x for x in output if x not in c.block)
        return output


    def open(self, game_number: int = 1, game_file='games.txt'):
        """
        :param game_number: A integer number of tha game inside the file
        :param game_file: The file to look for the game.

        Each game should be compose of the title and the rows of numbers, with the number 0 to
        represent empty cells. \n
        Exemple: \n
        "\n
        Grid 01\n
        003020600\n
        900305001\n
        001806400\n
        008102900\n
        700000008\n
        006708200\n
        002609500\n
        800203009\n
        005010300\n
        "\n
        """

        assert type(game_number) == int
        assert game_number >= 1

        with open(game_file) as f:
            for i in range((game_number-1)*10): f.readline()
            f.readline()

            numbers = []
            while len(numbers) < 81:
                v = f.read(1)
                if v != '\n':
                    numbers.append(int(v))
        self._build(numbers, True)


    def _build(self, nums=(0,)*81, solve_mode=False):
        """Used internally to construct the cells and their relationships"""

        self.cells  = tuple(Cell(nums[i]) for i in range(81))
        self.rows   = tuple(CellList(None for _x in range(9)) for _y in range(9))
        self.cols   = tuple(CellList(None for _x in range(9)) for _y in range(9))
        self.blocks = tuple(CellList(None for _x in range(9)) for _y in range(9))

        for i in range(81):
            x = i % 9
            y = i //9
            b0 = (x //3) + (y //3)*3
            b1 = (x % 3) + (y % 3)*3

            self.cells[i].row = self.rows[y]
            self.cells[i].row[x] = self.cells[i]

            self.cells[i].column = self.cols[x]
            self.cells[i].column[y] = self.cells[i]

            self.cells[i].block = self.blocks[b0]
            self.cells[i].block[b1] = self.cells[i]

            if solve_mode and self.cells[i].value != 0:
                self.cells[i].fixed = True


    def __str__(self):
        out = ''
        for i in range(9):
            if i%3 == 0:
                out += '+' + '---+'*3 + '\n'

            for j in range(9):
                if j%3 == 0:
                    out += '|'
                out += str(self.rows[i][j].value)

            out += '|\n'
        out += '+' + '---+' * 3 + '\n'
        return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--grid_number", type=int, help="Grid number from the given file to solve", default=1)
    parser.add_argument("-f", "--filename", help="The file to look for the games", type=str, default='games.txt')
    args = parser.parse_args()

    a = Sudoku()
    a.open(args.grid_number, args.filename)
    a.solve()
    print(a)