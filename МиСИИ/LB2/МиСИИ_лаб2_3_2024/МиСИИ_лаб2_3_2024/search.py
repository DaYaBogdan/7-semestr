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

    start = problem.getStartState()

    if problem.isGoalState(start): return []
    
    CLOSED = [start]

    for node in problem.getSuccessors(start):
        if node[0] in CLOSED: continue

        sub_path = depthSearch(problem, node, CLOSED)

        if sub_path is not None:
            return [node[1]] + sub_path

    return []


def depthSearch(problem, node, CLOSED: list) -> list:

    COORDS, WAY, _WEIGHT = node

    if problem.isGoalState(COORDS): return []

    CLOSED.append(COORDS)

    for child in problem.getSuccessors(COORDS):
        if child[0] in CLOSED: continue

        sub_path = depthSearch(problem, child, CLOSED)

        if sub_path is not None:
            return [child[1]] + sub_path

    return None

def hlam():
    # def depthSearch(problem, node, CLOSED: list) -> list:

    #     updatePath = path_updater()
    #     route = []

    #     # Раскрываем параметры ноды
    #     COORDS = node[0]
    #     WAY = node[1]
    #     WEIGHT = node[2]

    #     # Мы на месте?
    #     if problem.isGoalState(COORDS): return [WAY]

    #     # Раз мы не на месте, продолжим путь, зафиксируем место как посещённое
    #     CLOSED.append(COORDS)

    #     # Обход доступных мест | Если место уже посещено - пропуск
    #     for child in problem.getSuccessors(COORDS):
    #         if child[0] in CLOSED: continue

    #         # Поиск лучшего пути
    #         route = updatePath(depthSearch(problem, child, CLOSED))

    #     # Добавление в лучший путь нашей ноды | Если конечно такой существует
    #     if route: route.append(WAY)

    #     return route

    # def path_updater():
    #     path = []

    #     def updatePath(pathT: list) -> list:
    #         nonlocal path

    #         IS_VOID_LIST = not pathT
    #         if IS_VOID_LIST: return list(path)

    #         DONT_HAVE_ANY_PATH = not len(path)
    #         NEW_PATH_WEIGHTS_LESS = len(pathT) < len(path) 

    #         if DONT_HAVE_ANY_PATH or NEW_PATH_WEIGHTS_LESS: path = list(pathT)

    #         return list(path)

    #     return updatePath
    return 

from util import Queue
def breadthFirstSearch(problem):
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    OPEN = Queue()
    CLOSED = {start}
    parent = {}

    for child, action, _ in problem.getSuccessors(start):
        if child in CLOSED:
            continue
        CLOSED.add(child)
        parent[child] = (start, action)
        OPEN.push((child, action))

    while not OPEN.isEmpty():
        node, action = OPEN.pop()

        if problem.isGoalState(node):
            return Path(problem, node, parent)

        for child, child_action, _ in problem.getSuccessors(node):
            if child in CLOSED:
                continue
            CLOSED.add(child)
            parent[child] = (node, child_action)
            OPEN.push((child, child_action))

    return []

def Path(problem, node, parent):
    how_to_get_home = []
    start = problem.getStartState()

    while node != start:
        prev, action = parent[node]
        how_to_get_home.append(action)
        node = prev

    return how_to_get_home[::-1]

import heapq

def uniformCostSearch(problem):
    start = problem.getStartState()
    OPEN = util.Stack((0, start, []))          
    best_cost = {start: 0}               
    CLOSED = []

    while OPEN:
        cost, state, path = heapq.heappop(OPEN)

        if problem.isGoalState(state): return path

        if state in CLOSED: continue
        
        CLOSED.add(state)

        for succ, action, step_cost in problem.getSuccessors(state):
            new_cost = cost + step_cost
            if succ not in CLOSED and new_cost < best_cost.get(succ, float('inf')):
                best_cost[succ] = new_cost
                OPEN.push((new_cost, succ, path + [action]))

    return None

def nullHeuristic(state, problem=None):
    """
    Эвристическая функция оценивает стоимость от текущего состояния до 
    ближайшей цели в задаче SearchProblem. Эта эвристика тривиальна.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Находит узел с наименьшей комбинированной стоимостью, включающей эвристику
    """
    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
    util.raiseNotDefined()


#Аббривиатуры
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
