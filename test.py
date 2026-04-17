from mazegenerator import MazeGenerator

generator = MazeGenerator((20, 20), perfect=True)

# Generate the maze in a list format
maze = generator.generate_maze(seed=42)
