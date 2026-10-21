from typing import List, Tuple


class GraphOrdering:
    """Упорядочивание решений по ярусам (вершины-источники)."""

    def __init__(self, matrix: List[List[int]]):
        # matrix[i][j] == 1, если из вершины i в вершину j идёт дуга
        self.matrix = [row[:] for row in matrix]   # копия, чтобы не портить исходную
        self.n = len(matrix)

    # ------------------------------------------------------------------ #
    #  Основной алгоритм                                                  #
    # ------------------------------------------------------------------ #
    def build_ranking(self) -> List[Tuple[int, List[int]]]:
        matrix = [row[:] for row in self.matrix]   # локальная копия
        n = self.n

        ranking = []
        removed = [False] * n
        tier = 0

        while True:
            sources = []
            for j in range(n):
                if removed[j]:
                    continue
                if all(matrix[i][j] == 0 for i in range(n) if not removed[i]):
                    sources.append(j)

            if not sources:
                break

            tier += 1
            ranking.append((tier, sources))

            for q in sources:
                removed[q] = True
                for j in range(n):
                    matrix[q][j] = 0
                for i in range(n):
                    matrix[i][q] = 1

        return ranking

    # ------------------------------------------------------------------ #
    #  Вспомогательные методы                                             #
    # ------------------------------------------------------------------ #
    def ordered_decisions(self) -> List[int]:
        """Плоский упорядоченный список решений (лучшее — первым)."""
        ranking = self.build_ranking()
        return [v for _, tier in ranking for v in tier]

    def effective_decisions(self) -> List[int]:
        """Эффективные решения — вершины первого яруса (источники)."""
        ranking = self.build_ranking()
        return ranking[0][1] if ranking else []

    def print_result(self) -> None:
        ranking = self.build_ranking()
        print("Упорядоченное множество решений по ярусам:")
        for tier, vertices in ranking:
            names = [f"x{v + 1}" for v in vertices]
            print(f"  Ярус {tier}: {names}")

        ordered = [v for _, tier in ranking for v in tier]
        effective = ranking[0][1] if ranking else []

        print("\nПорядок решений (лучшее → худшее):",
            [f"x{v + 1}" for v in ordered])
        print("Эффективные решения (1-й ярус):",
            [f"x{v + 1}" for v in effective])