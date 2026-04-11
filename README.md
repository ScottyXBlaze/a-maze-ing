*This project has been created as part of the 42 curriculum by tiana-an, nyramana.*

# A-Maze-ing
> This is the way

## Description:

Lost in a maze? Not anymore. A_maze_ing generates and solves mazes from scratch — a deep dive into algorithmic thinking, memory management and path finding in Python

### How it works
The program generates a list of hexadecimal values representing the maze as strings.  
Each hexadecimal value is then converted to binary, which is used to determine the positions of the walls in the maze.  
___


For pathfinding, we implemented three algorithms ourselves:
-	Depth-First Search (**DFS**) – deep search
-	Breadth-First Search (**BFS**) – width search
-	A* Search (**A-star**) – A* search with heuristics

## Instruction:

### Makefile

The project includes a Makefile to simplify common tasks:

-	install: Install project dependencies using pip.
```bash
make install
```
-	run: Execute the main script of the project.
```bash
make run
```
-	debug: Run the main script in debug mode using Python’s built-in debugger (pdb).
```bash
make debug
```
-	clean: Remove temporary files or caches (e.g., \_\_pycache\_\_, .mypy_cache) to maintain a clean project environment.
```bash
make clean
```
-	lint: Run code quality and type checks using flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs.
```bash
make lint
```  
-	lint-strict (optional): Run stricter code quality checks using flake8 . and mypy . --strict.
```bash
make lint-strict  # Note: 'mlx' is a third-party library without type hints; related mypy warnings are expected.
```

- You can also run the program manually after setting up all the requirement using make install. To do this, just run
```bash
 python3 a_maze_ing.py config.txt  # You can change the name of the config file
```

## Resources:
The following resources were helpful for understanding:
-	[A-STAR algorithm](https://www.youtube.com/watch?v=-L-WgKMFuhE&t=123s)
-	[BFS algorithm](https://www.youtube.com/watch?v=D14YK-0MtcQ)
-	[DFS algorithm](https://www.youtube.com/watch?v=sTRK9mQgYuc)

>***AI usage:***  
    AI tools were used solely for conceptual explanations and learning support. The design, implementation, and final code were developed independently.

## File configuration:

All desired configurations should be placed in config.txt:
| Name 			| Type 			| Example 			|  Value    								|
|:-----			|:------:		|:------:			|--------:									|
| WIDTH   		|   int    		|  20   			|  (0 - 100)  								|
| HEIGHT  		|   int    		|  20   			|  (0 - 50)   								|
| ENTRY   		|   int, int  	|  0, 0  			|  (0 - (WIDTH - 1)), (0 - (HEIGHT - 1))    |
| EXIT    		|   int, int  	|  19, 19 			|  (0 - (WIDTH - 1)), (0 - (HEIGHT - 1))    |
| OUTPUT_FILE  	|   str    		|  maze_output.txt  |  None  									|
| PERFECT  		|   bool   		|  True   			|  True/False 1/0 y/n yes/no  				|
| SEED   		|   int    		|  42   			|  (0 for random)  							|
| ANIMATION   	|   bool   		|  True   			|  True/False 1/0 y/n yes/no  				|
| ALGO   		|   str   		|  AUTO   			|  DFS, BFS, ASTAR or AUTO  				|

## maze generation algorithm selection:
### ***`Hunt and kill:`***

### *Description:*
Hunt and kill is a popular algorithm to generate maze. It has two main stage: `hunt` and `kill` stage to make sure every cell is visited and linked with all other cells without having loops (perfect maze)

__`Hunt` stage__:
This hunt or search for unvisited cells that has a visited neighbor   
__`Kill` stage__:
Generate path with all the unvisited cells until it reaches a dead-end 

### *Justification:*
We chose the Hunt-and-Kill algorithm because it is simple to implement, memory-efficient, and generates perfect mazes with a good balance between randomness and structure. It also makes the seed implementation easier and we can control the generation to match what we want (direction or hunting algorithm).

###