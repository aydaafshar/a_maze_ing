*This project has been created as part of the 42 curriculum by ayafshar, eshinwar.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generation and solving application built in Python. The program generates random mazes using a randomized Depth-First Search (DFS) algorithm, solves them with BFS, and renders them in the terminal with ANSI color support. It supports both perfect mazes (exactly one solution) and imperfect mazes (with loops), configurable dimensions, entry/exit points, and reproducible generation via seeds.

The core maze logic is packaged as `mazegen`, a standalone pip-installable Python module with zero external dependencies, making it easy to reuse in other projects.

## Instructions

### Requirements

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation and Running

```bash
make install   # Install dependencies
make run       # Run the application
```

You can also pass a custom config file:

```bash
uv run python a_maze_ing.py my_config.txt
```

### Interactive Menu

Once running, the application presents an interactive menu:

1. **Re-generate** - Generate a new maze with a random seed
2. **Show/Hide solution** - Toggle the solution path overlay
3. **Rotate colors** - Cycle through wall color schemes (None, Yellow, Gray, White)
4. **Quit** - Exit the application

### Other Makefile Targets

```bash
make clean        # Remove build artifacts and __pycache__
make lint         # Run flake8 and mypy
make lint-strict  # Run mypy in strict mode
make build        # Build the mazegen pip package
```

## Configuration File

Edit `config.txt` to customize maze parameters. The format is simple `KEY=VALUE` pairs, with optional `#` comments:

```
# Maze configuration
WIDTH=20              # Maze width in cells (integer)
HEIGHT=15             # Maze height in cells (integer)
ENTRY=4,0             # Entry point as x,y coordinates
EXIT=10,10            # Exit point as x,y coordinates
OUTPUT_FILE=maze.txt  # Path for the output maze file
PERFECT=True          # True = perfect maze (no loops), False = ~10% random loops
```

| Key           | Type        | Default              | Description                                    |
|---------------|-------------|----------------------|------------------------------------------------|
| `WIDTH`       | int         | 20                   | Maze width in cells                            |
| `HEIGHT`      | int         | 15                   | Maze height in cells                           |
| `ENTRY`       | x,y         | 0,0                  | Entry point coordinates                        |
| `EXIT`        | x,y         | width-1, height-1    | Exit point coordinates                         |
| `OUTPUT_FILE` | string      | maze.txt             | Output file path for serialized maze           |
| `PERFECT`     | bool        | True                 | Perfect maze (no loops) or imperfect (~10% loops) |

## Maze Generation Algorithm

### Algorithm: Randomized Depth-First Search (DFS)

The maze is generated using a **Randomized Depth-First Search** (also known as recursive backtracker) algorithm:

1. Start at a random cell on the grid.
2. Mark the current cell as visited.
3. Randomly pick an unvisited neighbor, carve a passage to it, and move there.
4. If no unvisited neighbors remain, backtrack via the stack until one is found.
5. Repeat until all cells have been visited.

This produces a **spanning tree** of the grid, which guarantees a perfect maze: exactly one path between any two cells.

For **imperfect mazes** (`PERFECT=False`), approximately 10% of remaining walls are randomly removed to introduce loops and multiple solution paths.

An additional constraint prevents **wide corridors**: before carving into a cell, the algorithm checks whether doing so would create a 3x3 open area, preserving the classic narrow-corridor feel.

The **solver** uses Breadth-First Search (BFS) to find the shortest path from entry to exit.

### Why This Algorithm

- **Simplicity**: DFS-based generation is straightforward to implement and understand.
- **Quality**: It produces mazes with long, winding corridors and few dead-end clusters, which are visually appealing and interesting to solve.
- **Flexibility**: Easy to extend with loop injection for imperfect mazes.
- **Reproducibility**: Combined with a seeded random number generator, the same seed always produces the exact same maze.

## Reusable Module: `mazegen`

The `mazegen/` directory is a standalone, pip-installable Python package with **zero external dependencies**. It can be used independently in any Python project that needs maze generation or solving.

### Installation

```bash
# Install directly from source
pip install .

# Or build and install the wheel
pip install build
python -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Usage

```python
from mazegen import MazeGenerator

# Default maze (20x15, seed=42, perfect)
mg = MazeGenerator()

# Custom maze
mg = MazeGenerator(width=30, height=20, seed=123, perfect=False)

# Access cell walls
north, east, south, west = mg.cell_walls(5, 3)

# Get solution path as list of (x, y) coordinates
path = mg.solution

# Regenerate with a new seed
mg.regenerate(seed=99)

# Save to file
mg.save("output.txt")
```

### Package Structure

| Module         | Purpose                                        |
|----------------|------------------------------------------------|
| `__init__.py`  | `MazeGenerator` class - high-level API         |
| `maze.py`      | `Maze` data structure (2D grid of cells)       |
| `cell.py`      | `Cell` class with wall states and hex encoding |
| `direction.py` | `Direction` enum (N, E, S, W)                  |
| `generator.py` | DFS maze generation algorithm                  |
| `solver.py`    | BFS shortest-path solver                       |
| `writer.py`    | Maze serialization to hex-encoded file format  |

## Team and Project Management

### Team Roles

| Member       | Responsibilities                                         |
|--------------|----------------------------------------------------------|
| **ayafshar** | Maze generation algorithm, solver algorithm              |
| **eshinwar** | Configuration parser, terminal renderer, output writer   |

### Planning and Process

We started by breaking the project down into clearly separated tasks based on each member's role. After completing each phase, we held **pair programming sessions** to walk each other through our code, share knowledge, and ensure both members understood the full codebase.

**What worked well:**
- The clear task separation allowed us to work in parallel without conflicts.
- Pair programming sessions after each phase kept both members aligned and helped catch issues early.

**What could be improved:**
- Code readability could be improved with more consistent naming and documentation across modules.

### Tools

- **GitHub** - Version control and collaboration
- **WhatsApp** - Communication and coordination

## Resources

- [Maze generation algorithm - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm) - Overview of maze generation techniques including DFS
- [Think Labyrinth - Maze algorithms](http://www.astrolog.org/labyrnth/algrithm.htm) - Comprehensive reference on maze algorithms
- [Breadth-First Search - Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search) - BFS algorithm used for solving

### AI Usage

AI (Claude) was used during this project for the following tasks:

- **Requirement extraction**: Translating and clarifying project requirements from the subject document, which was difficult to parse due to translation issues.
- **Algorithm research**: Getting recommendations on which algorithms are commonly used for maze generation and their trade-offs, which informed the choice of Randomized DFS.

AI was not used to directly write the project code.
