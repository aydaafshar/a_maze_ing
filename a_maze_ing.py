import os
import sys

from src.config import Config
from mazegen import MazeGenerator


def main() -> None:
    from src.renderer import Renderer

    try:
        config_path = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
        config = Config()
        config.load(config_path)

        mg = MazeGenerator(
            config.width,
            config.height,
            config.entry,
            config.exit,
            42,
            config.perfect,
        )
        r = Renderer(mg.maze)

        show_solution = False

        mg.save(config.output_file)
        os.system("clear")
        r.render()

        while True:

            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            if not mg.maze.did_draw_42:
                print(
                    "\n\033[93mMaze size is too small"
                    " to draw the '42' in the middle\033[0m"
                )
            choice = input("Choice (1 - 4) ")

            if choice == "4":
                break

            if choice == "1":
                mg.regenerate()
                mg.save(config.output_file)
            elif choice == "2":
                show_solution = not show_solution
            elif choice == "3":
                r.rotate_colors()

            os.system("clear")
            if show_solution:
                r.render(mg.solution)
            else:
                r.render()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
