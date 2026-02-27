"""
mazegen - A maze generation and solving library.

Usage:
    from mazegen import MazeGenerator

    # Create a generator with default parameters (20x15 maze)
    mg = MazeGenerator()

    # Create with custom parameters
    mg = MazeGenerator(width=30, height=20, seed=42, perfect=True)

    # Access the maze object and its structure
    maze = mg.maze
    print(maze.width, maze.height)
    print(maze.entry, maze.exit)
    cell = maze.cells[y][x]
    print(cell.north, cell.east, cell.south, cell.west)  # wall states

    # Get a solution path from entry to exit
    path = mg.solution  # list of (x, y) coordinates

    # Regenerate with a new seed
    mg.regenerate(seed=123)
"""

from typing import List, Optional

from mazegen.maze import Coord, Maze
from mazegen.generator import Genarator
from mazegen.solver import Solver
from mazegen.writer import Writer

__all__ = ["MazeGenerator", "Coord", "Maze"]


class MazeGenerator:
    """A reusable maze generator with built-in solver.

    Args:
        width: Maze width in cells (default: 20).
        height: Maze height in cells (default: 15).
        entry: Entry coordinate as (x, y) tuple (default: top-left corner).
        exit: Exit coordinate as (x, y) tuple (default: bottom-right corner).
        seed: Random seed for reproducible generation (default: 42).
        perfect: If True, generate a perfect maze (no loops). If False,
                 add ~10% random loops (default: True).
    """

    def __init__(
        self,
        width: int = 20,
        height: int = 15,
        entry: Optional[Coord] = None,
        exit: Optional[Coord] = None,
        seed: int = 42,
        perfect: bool = True,
    ) -> None:
        if entry is None:
            entry = (0, 0)
        if exit is None:
            exit = (width - 1, height - 1)

        self._maze = Maze(width, height, entry, exit, perfect)
        self._generator = Genarator(self._maze)
        self._solver = Solver(self._maze)
        self._writer = Writer(self._maze)
        self._solution: List[Coord] = []
        self._seed = seed

        self._generator.generate(seed)
        self._solution = self._solver.solve()

    @property
    def maze(self) -> Maze:
        """The underlying Maze object.

        Provides access to all maze attributes:
        - maze.width, maze.height: dimensions
        - maze.entry, maze.exit: coordinates (x, y)
        - maze.perfect: whether the maze has no loops
        - maze.cells: 2D grid of Cell objects (cells[y][x])
        - maze.in_bounds(x, y): boundary check
        - maze.neighbors(x, y): adjacent cells
        """
        return self._maze

    @property
    def seed(self) -> int:
        """Current random seed."""
        return self._seed

    @property
    def solution(self) -> List[Coord]:
        """Solution path as a list of (x, y) coordinates from entry to exit."""
        return self._solution

    def regenerate(self, seed: Optional[int] = None) -> None:
        """Regenerate the maze with a new or specified seed.

        Args:
            seed: New random seed. If None, uses the current seed + 1.
        """
        if seed is not None:
            self._seed = seed
        else:
            self._seed += 1
        self._generator.generate(self._seed)
        self._solution = self._solver.solve()

    def save(self, output_file: str) -> None:
        """Save the maze and its solution to a file.

        Args:
            output_file: Path to the output file.
        """
        self._writer.save(self._solution, output_file)
