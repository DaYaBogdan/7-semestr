from typing import List, Tuple

class Max_R_X:

    #--------------------------------------------
    # Константы для работы класса
    #--------------------------------------------

    def __init__(self, matrix):
        self.matrix = matrix
        self.max = len(matrix)

    #--------------------------------------------
    # Для второй части работы
    #--------------------------------------------

    def __findMaxIncidence(self) ->list:
        matrix = [row[:] for row in self.matrix]
        max = self.max

        ranking = []
        removed = [False] * max
        tier = 0

        while True:
            sources = []
            for j in range(max):
                if removed[j]:
                    continue
                if all(matrix[i][j] == 0 for i in range(max) if not removed[i]):
                    sources.append(j)

            if not sources:
                break

            tier += 1
            ranking.append((tier, sources))

            for q in sources:
                removed[q] = True
                for j in range(max):
                    matrix[q][j] = 0
                for i in range(max):
                    matrix[i][q] = 1

        return ranking

    def ordered_decisions(self) -> List[int]:
            """Плоский упорядоченный список решений (лучшее — первым)."""
            ranking = self.__findMaxIncidence()
            return [v for _, tier in ranking for v in tier]
    
    def effective_decisions(self) -> List[int]:
        """Эффективные решения — вершины первого яруса (источники)."""
        ranking = self.__findMaxIncidence()
        return ranking[0][1] if ranking else []

    def print_result(self) -> None:
        ranking = self.__findMaxIncidence()
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

    #--------------------------------------------
    # Для первой части работы
    #--------------------------------------------
    
    def findMax(self) -> list:
        matrix = self.matrix
        max = [1 for i in range(len(self.matrix))]
        
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    if matrix[j][i] == 0: 
                        max[j] = 0
                    if matrix[j][i] == 1 and max[i] == 0:
                        max[j] = 0

        return max