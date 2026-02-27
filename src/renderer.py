from typing import FrozenSet, List, Set

from mazegen.maze import Coord
from mazegen.maze import Maze

WALL_COLORS = [
    None,
    "\033[93m",  # yellow
    "\033[90m",  # red
    "\033[97m",  # white
]
RESET = "\033[0m"
SPACE = " "
FROZEN = "▒"
START = "\033[92m█\033[0m"
END = "\033[91m█\033[0m"
PATH = "\033[94m█\033[0m"


class Renderer:
    def __init__(self, maze: Maze):
        self.maze = maze
        self._wall_color_index = 0

    def rotate_colors(self) -> None:
        self._wall_color_index = (self._wall_color_index + 1) % len(
            WALL_COLORS
        )

    def _wall_char(self) -> str:
        color = WALL_COLORS[self._wall_color_index]
        if color is None:
            return "█"
        return f"{color}█{RESET}"

    def render(self, solution: List[Coord] = []):
        self._path_set: Set[Coord] = set(solution)
        self._path_edges: Set[FrozenSet] = set()
        for i in range(len(solution) - 1):
            self._path_edges.add(frozenset((solution[i], solution[i + 1])))
        w = self._wall_char()
        print(w * (self.maze.width * 2 + 1))
        for y in range(self.maze.height):
            self._render_cell_line(y)
            self._render_wall_line(y)

    def _is_path_edge(self, a: Coord, b: Coord) -> bool:
        return frozenset((a, b)) in self._path_edges

    def _cell_char(self, x: int, y: int) -> str:
        coord = (x, y)
        if coord == self.maze.entry:
            return START
        if coord == self.maze.exit:
            return END
        if coord in self._path_set:
            return PATH
        if self.maze.cells[y][x].locked:
            return FROZEN
        return SPACE

    def _render_cell_line(self, y: int):
        line = ""
        for x in range(self.maze.width):
            cell = self.maze.cells[y][x]
            if x == 0:
                line += self._wall_char() if cell.west else SPACE
            line += self._cell_char(x, y)
            if (
                not cell.east
                and x < self.maze.width - 1
                and self._is_path_edge((x, y), (x + 1, y))
            ):
                line += PATH
            else:
                line += self._wall_char() if cell.east else SPACE
        print(line)

    def _render_wall_line(self, y: int):
        ny = y + 1
        line = ""
        for x in range(self.maze.width):
            cell = self.maze.cells[y][x]
            has_wall = cell.south
            if x == 0:
                line += self._wall_char() if has_wall or cell.west else SPACE
            if (
                not has_wall
                and self.maze.in_bounds(x, ny)
                and self._is_path_edge((x, y), (x, ny))
            ):
                line += PATH
            else:
                line += self._wall_char() if has_wall else SPACE
            has_corner = has_wall or cell.east
            if x < self.maze.width - 1:
                next_cell = self.maze.cells[y][x + 1]
                has_corner = has_corner or next_cell.south
            line += self._wall_char() if has_corner else SPACE
        print(line)
