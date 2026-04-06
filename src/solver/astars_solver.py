# heapq est un module qui permet de tranformer une liste en une tas (heap)
# le heapq implemente specifiquement le min-heap qui permet de trier automatiquement
# le tas pour pouvoir acceder rapidement a l'element le plus petit d'une collection
# L'element le plus petit se trouve toujours a l'index 0 ou racine

import heapq
from typing import List, Tuple, Optional
from .base_solver import BaseSolver


class AStarSolver(BaseSolver):
    """A Stars algorithm is probably the most used algo to solve
    path efficiently. it gives the most optimal path without
    checking all the cells of the maze, it is faster than BFS
    because of his pathfinding method and can be easily implemented
    with some easy math

    Args:
        BaseSolver (Class): The base of all the solver
    """

    def heuristic(self, pos: Tuple[int, int]) -> int:
        """Calculate the distance between a postion and
        the ending of the maze using the Manhattan distance

        Args:
            pos (Tuple[int, int]): the postion to do the math

        Returns:
            int: the distance between the pos and the ending
        """
        return abs(pos[0] - self.ending[0]) + abs(pos[1] - self.ending[1])

    def solve(self) -> Optional[List[str]]:
        """This solve the entire maze, it calculate the cost of each cell
        using a formula and prioritize the cell that has the minimal cost
        estimation to finish the maze, it can optimize the program
        because we don't have to checks every cells but we can still
        find the most optimal path

        Returns:
            Optional[List[str]]: the path in a list or None if no path was found
        """
        start = self.starting
        goal = self.ending

        # `open_set` est la file de priorité (min-heap).
        # Chaque élément est un tuple :
        # (f, g, position, chemin)
        # f = score estimé total, g = coût réel déjà parcouru.
        # On va ajouter le heapq sur ce liste
        open_set = []

        # On commence au point de départ :
        # g = 0 (on n'a pas bougé),
        # f = h(start),
        # chemin vide.
        heapq.heappush(open_set, (0 + self.heuristic(start), 0, start, []))

        # Ensemble des cases déjà traitées définitivement.
        # Quand une case est dans `visited`, on ne la retravaille plus.
        visited = set()

        while open_set:
            # On récupère la case la plus prometteuse (plus petit score f).
            # le premier argument est l'estimation du total cost, mais on n'a
            # pas specialement besoin voila porquoi je ne l'ai pas fait dans
            # notre code
            _, cost_so_far, current, path = heapq.heappop(open_set)

            # Si notre position initiale est deja dans le liste des cellules
            # visiter, on ne fait rien et continue de prendre les autres cellules
            if current in visited:
                continue
            # Si ce n'est pas visitee on continue le code ajoute le position
            # avec les les cases visitee
            visited.add(current)

            # Si on a atteint l'arrivée, le chemin accumulé est la solution.
            if current == goal:
                return path

            # On regarde les voisins accessibles de la case courante.
            # `direction` = lettre (N/S/E/W), `neighbor` = coordonnée voisine.
            for direction, neighbor in self.neighbors(current):
                # Pareille comme celle en haut
                if neighbor in visited:
                    continue

                # Nouveau coût réel g : un déplacement supplémentaire (+1).
                new_cost = cost_so_far + 1

                # On ajoute la direction empruntée au chemin courant.
                # Exemple le path est vide et on ajoute le chemin 'N' qui va donner ['N']
                # et ainsi de suite
                new_path = path + [direction]

                # Priorité A* : f = g + h
                # g : coût réel jusqu'au voisin
                # h : estimation de ce qu'il reste jusqu'à l'arrivée
                priority = new_cost + self.heuristic(neighbor)

                # On remet ce voisin dans la file de priorité.
                heapq.heappush(open_set, (priority, new_cost, neighbor, new_path))
                # On recomence j'usqua ce que le chemin est trouvé ou il n'y a plus rien
                # dans le heap

        return None  # Aucun chemin trouvé

    def solve_as_string(self) -> str:
        """Solve the maze and transorm the path into a string

        Returns:
            str: the formated string
        """
        path = self.solve()
        if path is None:
            return ""
        return "".join(path)
