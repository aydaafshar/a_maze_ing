from collections import deque
from typing import Deque, Dict, List, Optional, Set

from mazegen.maze import Coord, Maze


class Solver:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def solve(self) -> List[Coord]:
        queue: Deque[Coord] = deque([self.maze.entry])
        visited: Set[Coord] = {self.maze.entry}
        parent: Dict[Coord, Optional[Coord]] = {self.maze.entry: None}

        while queue:
            current: Coord = queue.popleft()

            if current == self.maze.exit:
                path: List[Coord] = []
                cur: Optional[Coord] = current

                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]

                path.reverse()
                return path

            x, y = current
            cell = self.maze.cells[y][x]

            for d, nx, ny in self.maze.neighbors(x, y):
                neighbor: Coord = (nx, ny)

                if neighbor not in visited and not cell.is_closed(d):
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return []
