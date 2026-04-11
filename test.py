import mazegen

maze = mazegen.MazeGenerator((100, 100), False)
grid = maze.generate_maze()
for line in grid:
    for cell in line:
        print(cell, end="")
    print()
