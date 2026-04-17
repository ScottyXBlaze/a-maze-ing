 *This project has been created as part of the 42 curriculum by tiana-an, nyramana.* 

# A-Maze-ing

> The amazing world of maze!

## Description:

Lost in a maze? A-Maze-ing generates and solves mazes from scratch and showcases algorithmic design, pathfinding, and visualization in Python.

This project provides:

- A modular maze generator (Hunt-and-Kill).
- Three pathfinding implementations: DFS, BFS and A*.
- A small rendering layer (MLX-based) with optional animations and visual controls.

### How it works

The generator outputs hexadecimal strings that encode wall placements. Each hex value is converted to binary to determine walls for each cell. The solver modules then traverse the generated maze using the selected algorithm and can render the search and final path.

___

For pathfinding we implemented three algorithms:

- Depth-First Search (DFS) — depth-oriented exploration.
- Breadth-First Search (BFS) — level-by-level exploration (finds shortest path in unweighted grids).
- A* (A-star) — heuristic-guided search (balances distance traveled and estimated distance to goal).

## Instruction:

### Makefile

Common targets are:

- `make install` — install project dependencies via pip.
- `make run` — run the main script using the configuration file.
- `make debug` — run the program under Python's debugger (`pdb`).
- `make clean` — remove temporary files and caches (e.g. __pycache__, .mypy_cache).
- `make lint` — run `flake8` and `mypy` with the project's preferred options.
- `make lint-strict` — stricter linting (note: the bundled `mlx` wheel has no type hints and may produce mypy warnings).

You can also run the program directly after installing dependencies:

```bash
python3 a_maze_ing.py config.txt
```

Replace `config.txt` with another configuration file if desired.

## Resources:

Helpful resources used while implementing algorithms:

- [A* algorithm overview](https://www.youtube.com/watch?v=-L-WgKMFuhE&t=123s)
- [BFS explanation](https://www.youtube.com/watch?v=D14YK-0MtcQ)
- [DFS explanation](https://www.youtube.com/watch?v=sTRK9mQgYuc)

> ***AI usage:***

AI tools assisted with conceptual explanations only. All code and design decisions were implemented by the authors.

## File configuration:

All runtime configuration is read from the **configuration file**. Expected keys and types:

| Name | Type | Example | Valid values |
|:-----|:-----:|:-------:|:------------:|
| WIDTH | int | 20 | 0–100 |
| HEIGHT | int | 20 | 0–50 |
| ENTRY | int,int | 0,0 | 0–(WIDTH-1), 0–(HEIGHT-1) |
| EXIT | int,int | 19,19 | 0–(WIDTH-1), 0–(HEIGHT-1) |
| OUTPUT_FILE | str | maze_output.txt | (path or filename) |
| PERFECT | bool | True | True/False (also accepts 1/0, y/n, yes/no) |
| SEED | int | 42 | 0 for random, or any integer |
| ANIMATION | bool | True | True/False (1/0, y/n) |
| ALGO | str | AUTO | DFS, BFS, ASTAR or AUTO |

## maze generation algorithm selection:

### *** `Hunt and kill:` ***

### *Description:*

Hunt-and-Kill combines random walk (kill) with a periodic scan (hunt) to ensure all cells are visited. It produces a perfect maze (no loops, single path between cells) with low memory overhead.

__`Hunt` stage:__ search for an unvisited cell that neighbors a visited cell.

__`Kill` stage:__ perform a randomized walk from that cell until reaching a dead end, carving passages as you go.

### *Why this algorithm?*

- Simple to implement and memory efficient.
- Produces visually interesting mazes with good randomness.
- Works well with seed-based reproducibility.

## Reusability:

Most components are modular and reusable outside this project:

- The generator is independent of rendering and can be reused to produce grid mazes.
- Grid and neighbor utilities are generic and applicable to other grid-based problems.
- Solver implementations are separated and can be used standalone with any maze representation matching the expected API.

Only `a_maze_ing.py` and `input_validation.py` contain application-specific input handling.

## Team and project management:

### The roles of each team member:

All contributors collaborated across design, implementation and testing.

***More precision? Ok, here they are:***

---
** `tiana-an` **

- Implemented rendering logic that decodes hex-encoded wall data.
- Contributed to maze string generation and visual layout.
- Implemented the 42 logo rendering at the maze center.

---
** `nyramana` **

- Contributed to maze generation.
- Implemented pathfinding algorithms and solver logic.
- Led visual design, colors and animation tuning.

---

### Anticipated planning and evolution

Initial work focused on understanding MLX rendering and encoding walls using hex strings. After stabilizing generation, the team implemented and iterated on solvers (BFS, DFS, A*), followed by visual improvements and animations.

## Specific tools used:

- MLX (provided in the project) for rendering.
- Standard Python tooling: flake8, mypy, and pip for dependency management.

## Advanced Features

Implemented pathfinding options and visualization features:

- **BFS** — finds shortest path in unweighted mazes, explores breadth-first.
- **DFS** — simple depth-first search, useful for exploration behavior but not guaranteed shortest.
- **A*** — heuristic-guided search combining actual cost and estimated cost: $f(n)=g(n)+h(n)$ where $g$ is the path cost and $h$ is the heuristic estimate.

***Runtime Help / Usage Information:***

At runtime the program prints interactive instructions and shortcuts to control visualization, animation and color options.

## Bonus Features

- **Multiple Pathfinding Algorithms** — choose between BFS, DFS and A*.
- **Path Animation** — watch the solver discover the path in real time.
- **Customizable Visualization** — adjust colors and background during runtime.
- **Background & Color Harmony** — custom XPM-based backgrounds for consistent visuals.
- **Visited-cell Visualization** — optionally animate visited cells before drawing the final path.

---

