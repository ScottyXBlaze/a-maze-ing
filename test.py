from src import AStarSolver, BFSSolver
from mazegen import MazeGenerator

if __name__ == "__main__":
    maze = MazeGenerator((20, 20), perfect=False).generate_maze()
    a_stars = AStarSolver(maze, (0, 0), (19, 19))
    dfs = BFSSolver(maze, (0, 0), (19, 19))
    print("DFS path:", dfs.solve_as_string())
    print(f"Length of DFS path: {len(dfs.solve()) if dfs.solve() else 'NO PATH'}")
    print("A* path:", a_stars.solve_as_string())
    print(f"Length of A* path: {len(a_stars.solve()) if a_stars.solve() else 'NO PATH'}")