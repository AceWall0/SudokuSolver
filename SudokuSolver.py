from random import choice


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

    def __init__(self, v=0):
        self.value = v
        self.memory = []

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


def load_game(n=1):
    with open('games.txt') as f:
        # skip lines
        for i in range((n-1)*10): f.readline()
        print(f.readline())

        out = []
        while len(out) < 81:
            v = f.read(1)
            if v != '\n':
                out.append(int(v))
    print(out)
    return out


def parse_game(char):
    i = 0
    while i < 81:
        if char != '\n':
            i += 1
            yield int(char)


def main(game_number=0):

    if game_number > 0:
        solve = True
        game = load_game(game_number)
    else:
        solve = False
        game = (0,)*81

    cells = tuple(Cell(game[i]) for i in range(81))

    rows   = tuple(CellList(None for _x in range(9)) for _y in range(9))
    cols   = tuple(CellList(None for _x in range(9)) for _y in range(9))
    blocks = tuple(CellList(None for _x in range(9)) for _y in range(9))

    for i in range(81):
        x = i % 9
        y = i //9
        b0 = (x //3) + (y //3)*3
        b1 = (x % 3) + (y % 3)*3

        cells[i].row = rows[y]
        cells[i].row[x] = cells[i]

        cells[i].column = cols[x]
        cells[i].column[y] = cells[i]

        cells[i].block = blocks[b0]
        cells[i].block[b1] = cells[i]

        if solve and cells[i].value != 0:
            cells[i].fixed = True

    options = tuple(range(1, 10))

    i = 0
    direction = 1
    while i < 81:
        cell = cells[i]

        if cell.fixed:
            i += direction
            continue

        available = tuple(x for x in options if x not in cell.memory)
        available = tuple(x for x in available if x not in cell.row)
        available = tuple(x for x in available if x not in cell.column)
        available = tuple(x for x in available if x not in cell.block)

        if available:
            val = choice(available)
            cell.value = val
            cell.memory.append(val)
            direction = 1

        else:
            cell.value = 0
            cell.memory = []
            direction = -1

        i += direction

    print(*rows, sep='\n')


if __name__ == '__main__':
    main(2)