from random import choice, seed
seed(1)

class CellList(list):
    """
    A list that when the "in" operator is called, looks for the item in the .value property of the elements in the list,
    as oppose to looking for the elements of the list"""

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

    def solve2(self):
        """
        Solves the game previously builded.
        This solution tries to minimize the number of backtracking by putting the values in the cells with the smaller
        values available
        """

        k = 0               # used for backtracking
        steps = []
        guesses = []        # what k values the algorithm made a guess
        guess_thr = 1       # the minimal number of available it should guess
        last_ind = -1       # the last index where a value was changed
        completed = False   # has the code been completed?

        while not completed:
            completed = True

            while True:
                i = k % 81

                # has made a entire loop without changing a value
                if i == last_ind: guess_thr += 1

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



    def generate(self):
        self._build()
        self.solve1()


    def __filter_options(self, c):
        options = tuple(range(1, 10))
        output = tuple(x for x in options if x not in c.memory)
        output = tuple(x for x in output if x not in c.row)
        output = tuple(x for x in output if x not in c.column)
        output = tuple(x for x in output if x not in c.block)
        return output


    def open_game(self, game_number: int, game_file='games.txt'):
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


    def print(self):
        print(*self.rows, sep='\n')


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
    a = Sudoku()
    a.open_game(1)
    a.solve2()
    print(a)