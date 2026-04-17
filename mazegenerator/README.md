 *This project has been created as part of the 42 curriculum by nyramana, tiana-an.* 

# MazeGenerator:

## Description:

MazeGenerator is a simple library that generate a maze from a given configuration. The maze is generated in a 2D grid with every cells represented as an hexadecimal integer.

### Interpretation:

| Direction | index (LSB) |
|:-----------------|-------------:|
|North|0|
|East|1|
|South|2|
|West|3|

 **The bit `1` means closed and the bit `0` means open.** 

### Example:

* 16 (1111) has every direction closed
* 0  (0000) has every direction open
* 13 (1101) have a wall closed on east
* 6  (0110) has a cell open at east and south and close in the other direction

### Algorithm:

#### ! HUNT AND KILL !

The Hunt-and-Kill algorithm is an iterative, cell-based method used to generate perfect mazes (mazes with no loops and no inaccessible areas). It strikes a balance between the organic, winding paths of a Depth-First Search and the efficiency of more grid-based methods.
The Algorithm: Step-by-Step

* **`Start`** : Choose an initial starting cell at random and mark it as Visited.

* **`Kill Mode`** : Perform a random walk from the current cell. At each step, move to an adjacent Unvisited neighbor, carve a path (remove the wall), and mark the new cell as Visited. Repeat this until the current cell has no Unvisited neighbors.

* **`Hunt Mode`** : Scan the grid usually from top-left to bottom-right to find an Unvisited cell that is adjacent to at least one Visited cell. If such a cell is found, carve a path between it and its visited neighbor, mark it as Visited, and make it the new "current cell." Return to Kill Mode.

* **`Termination`** : The algorithm finishes when the "Hunt" scan completes without finding any more unvisited cells.

#### Umperfect maze!?:
Creating an umperfect cell is really easy. After creating the perfect maze using the `hunt and kill` method, we just choose a random cell, pick a random wall and break it. It is made so that every maze can be redone by using the random method using seed and we can easily change the amount of cell we want to delete.

## Instruction:

First insall the `.whl` file or copy the folder into your project. Then import the library `mazegenerator` and that's all you need to use all the generation and methods inside it. 

 **Example:** 

```python
from mazegenerator import Mazegenerator

generator = MazeGenerator((20, 20), perfect=True)

# Generate the maze in a 2D list format
maze = generator.generate_maze(seed=42)

for grid in maze:
    for line in grid:
        print(line, end="")
    print()
```

### Available methods:

```python

from mazegenerator import MazeGenerator

generator = MazeGenerator((20, 20), perfect=True)

# Generate a grid full of the caractere `F`
_ = generator.generate_grid()

# Return all the cells to form the 42 positions to the cells 
_ = generator.get_forty_two_positions()

# Generates the maze
_ = generator.generate_maze(seed=42)

```

## Ressources:
