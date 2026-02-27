from typing import List

from mazegen.maze import Coord
from mazegen.maze import Maze


class Writer:
    def __init__(self, maze: Maze):
        self.maze = maze

    def save(self, solution: List[Coord], output_file: str) -> None:
        with open(output_file, "w") as f:
            for y in range(self.maze.height):
                row_bits = []
                for x in range(self.maze.width):
                    row_bits.append(self.maze.cells[y][x].to_bits())
                f.write("".join(row_bits) + "\n")

            f.write("\n")

            ex, ey = self.maze.entry
            f.write(f"{ex} {ey}\n")

            tx, ty = self.maze.exit
            f.write(f"{tx} {ty}\n")

            directions = []
            for i in range(len(solution) - 1):
                cx, cy = solution[i]
                nx, ny = solution[i + 1]
                dx, dy = nx - cx, ny - cy
                if dx == 1:
                    directions.append("E")
                elif dx == -1:
                    directions.append("W")
                elif dy == 1:
                    directions.append("S")
                else:
                    directions.append("N")
            f.write("".join(directions) + "\n")
