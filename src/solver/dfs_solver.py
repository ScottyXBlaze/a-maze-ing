from typing import List, Optional, Tuple
from .base_solver import BaseSolver


class DFSSolver(BaseSolver):
    """The DFS algorithm who is used for basic maze
      It is not as good as other algorithm but it is
      easy to lean and understand and can easily solve
      perfect maze and unperfect one (but not the most optimal
      path sadly)

    Args:
        BaseSolver (Class): The base class of all the Solver algorithm
    """

    def solve(self) -> Optional[List[str]]:
        """This solve the entire maze, it is done by checking random
        path and traverse them until he reach a dead-end, then go back
        until he founds another unvisited path and wander there. the algo end
        only if he founds the path or that every available cells are visited

        Returns:
            Optional[List[str]]: the path in a list or None if no path was found
        """
        # Gestion d'erreur juste au cas ou
        if (
            not self.maze
            or not self._is_valid_pos(*self.starting)
            or not self._is_valid_pos(*self.ending)
        ):
            return None

        if self.starting == self.ending:
            return []

        # STACK pour DFS (Last In First Out)
        # Chaque élément contient : (position actuelle, chemin accumulé)
        stack = [(self.starting, [])]
        
        # Ensemble des cases déjà visitées
        visited = {self.starting}

        while stack:
            # DFS : on prend le DERNIER élément ajouté (LIFO)
            current_pos, path = stack.pop()

            # Si on a atteint l'arrivée, retourner le chemin
            if current_pos == self.ending:
                return path

            # Explorer les voisins
            for direction, neighbor in self.neighbors(current_pos):
                if neighbor in visited:
                    continue

                # Marquer le voisin comme visité
                visited.add(neighbor)

                # Ajouter le voisin à la stack avec le nouveau chemin
                new_path = path + [direction]
                stack.append((neighbor, new_path))

        # Aucun chemin trouvé
        return None

    def solve_as_string(self) -> str:
        """Convert the path into a string

        Returns:
            str: the path combined
        """
        path = self.solve()
        if path is None:
            return ""
        return ''.join(path)
