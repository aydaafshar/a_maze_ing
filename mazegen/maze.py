import math
from typing import List, Tuple
from mazegen.cell import Cell
from mazegen.direction import Direction

Coord = Tuple[int, int]


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Coord,
        exit: Coord,
        perfect: bool = True,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.did_draw_42: bool = True

        if width <= 0 or height <= 0:
            raise ValueError("width/height must be > 0")

        ex, ey = entry
        tx, ty = exit
        if not self.in_bounds(ex, ey) or not self.in_bounds(tx, ty):
            raise ValueError("entry/exit must be inside maze bounds")
        if entry == exit:
            raise ValueError("entry and exit must be different")

        self.cells: List[List[Cell]] = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(Cell())
            self.cells.append(row)
        self._draw_42()
        self._enforce_borders_closed()

        if self.cells[ty][tx].locked:
            raise ValueError("Exit cannot be on 42 sign.")
        if self.cells[ey][ex].locked:
            raise ValueError("Entry cannot be on 42 sign.")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, x: int, y: int) -> List[Tuple[Direction, int, int]]:
        result = []
        for d in Direction:
            nx, ny = x + d.dx, y + d.dy
            if self.in_bounds(nx, ny):
                result.append((d, nx, ny))
        return result

    def _enforce_borders_closed(self) -> None:
        for x in range(self.width):
            self.cells[0][x].north = True
        for x in range(self.width):
            self.cells[self.height - 1][x].south = True
        for y in range(self.height):
            self.cells[y][0].west = True
        for y in range(self.height):
            self.cells[y][self.width - 1].east = True

    def carve(self, x: int, y: int, d: Direction) -> None:
        nx, ny = x + d.dx, y + d.dy
        if not self.in_bounds(nx, ny):
            raise ValueError("cannot carve outside maze bounds")
        if self.cells[y][x].locked or self.cells[ny][nx].locked:
            raise AssertionError("Cannot carve the the locked cells")
        self.cells[y][x].set_wall(d, False)
        self.cells[ny][nx].set_wall(Direction.opposite(d), False)
        self._enforce_borders_closed()

    def fill(self, x: int, y: int) -> None:
        if not self.in_bounds(x, y):
            return

        c = self.cells[y][x]
        c.north = c.east = c.south = c.west = True

        for d, nx, ny in self.neighbors(x, y):
            self.cells[ny][nx].set_wall(Direction.opposite(d), True)
        c.lock()
        self._enforce_borders_closed()

    def reset(self):
        for row in self.cells:
            for cell in row:
                cell.reset()

    def _draw_42(self):
        # rect 7x5
        H = 5
        W = 7
        if self.width <= W + 1 or self.height <= H + 1:
            self.did_draw_42 = False
            return
        cx = math.ceil((self.width - W) / 2)
        cy = math.ceil((self.height - H) / 2)
        coords: List[Coord] = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2),
            (2, 3),
            (2, 4),
            (4, 0),
            (5, 0),
            (6, 0),
            (6, 1),
            (6, 2),
            (5, 2),
            (4, 2),
            (4, 3),
            (4, 4),
            (5, 4),
            (6, 4),
        ]

        for x, y in coords:
            self.fill(x + cx, y + cy)
