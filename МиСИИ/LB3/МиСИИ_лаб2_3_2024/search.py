# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
В search.py вам необходимо реализовать общие алгоритмы поиска, которые вызываются
агентом Pacman (в searchAgents.py).
"""

import util

class SearchProblem:
    """
    Этот класс описывает структуру задачи поиска, но не реализует 
    ни один из методов (в объектно-ориентированной терминологии: абстрактный класс).

     Вам не нужно ничего менять в этом классе.
    """

    def getStartState(self):
        """
        Возвращает начальное состояние для задачи поиска.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: состоние

        Возвращает True, когда состояние является допустимым целевым состоянием.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: состояние

        Для данного состояния возвращает список из триплетов (successor,
        action, stepCost), где 'successor' - это преемник текущего
        состояния, 'action' - это действие, необходимое для этого, а "stepCost" - 
        затраты раскрытия преемника.
        
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions:Список действий, которые нужно предпринять

         Этот метод возвращает общую стоимость определенной последовательности
         действий. Последовательность должна состоять из разрешенных ходов.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Поиск в глубину. 

    Ваш алгоритм поиска должен возвращать список действий, которые 
    ведут к цели. Убедитесь, что реализуете алгоритм поиска на графе

    Прежде чем кодировать,полезно выполнить функцию  с этими простыми
    командами,чтобы понять смысл задачи (problem), передаваемой на вход:
    
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Находит самые поверхностные узлы в дереве поиска """
    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Находит узел минимальной стоимости """
    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    Эвристическая функция оценивает стоимость от текущего состояния до 
    ближайшей цели в задаче SearchProblem. Эта эвристика тривиальна.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    start = problem.getStartState()
    OPEN = util.PriorityQueue()
    OPEN.push((start, [], 0), heuristic(start, problem))
    best_g = {start: 0}
    CLOSED = set()

    while not OPEN.isEmpty():
        state, path, g = OPEN.pop()

        if g > best_g.get(state, float('inf')): continue

        if problem.isGoalState(state): return path

        if state in CLOSED: continue
        
        CLOSED.add(state)

        for succ, action, step_cost in problem.getSuccessors(state):
            new_g = g + step_cost
            if succ in CLOSED: continue
            if new_g < best_g.get(succ, float('inf')):
                best_g[succ] = new_g
                new_f = new_g + heuristic(succ, problem)
                OPEN.update((succ, path + [action], new_g), new_f)

    return None

#Аббривиатуры
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
