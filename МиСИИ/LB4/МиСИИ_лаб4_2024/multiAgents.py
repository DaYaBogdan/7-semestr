# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    Рефлекторный агент выбирает действие в каждой точке выбора,
    исследуя альтернативы с помощью функции оценки состояния.

    Приведенный ниже код предоставляется в качестве руководства.
    Вы можете изменить его так, как считаете нужным, при условии,
    что вы не касаетесь заголовков наших методов.
    """

    def getAction(self, gameState):
        """
        Вам не нужно менять этот метод, но вы можете это сделать.

        getAction возвращает одно из лучших действий в соответствии с
        функцией оценки.

        getAction принимает состояние GameState и
        возвращает направления Directions.X для некоторого X из мно-ва
        {NORTH, SOUTH, WEST, EAST, STOP}
       """
        # Получить допустимые действия для состояния
        legalMoves = gameState.getLegalActions()
        
        # print("legalMoves: ", legalMoves)

        # Выбрать одно из лучших действий в состоянии, используя функцию оценки
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print("Scores: ", scores)
        
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Случайно выбираем действие среди лучших

        "Добавьте свой код сюда, если хотите"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Разработайте здесь более совершенную функцию оценки.
        
        Функция оценки принимает текущее состояние и допустимое действие
        (pacman.py) и возвращает числовое значение функции оценки
        (большим числам отдается предпочтение).

        Приведенный ниже код извлекает некоторую полезную информацию из 
        состояния, такую как оставшаяся еда (newFood) и положение Pacman после
        перемещения (newPos).
        newScaredTimes содержит количество ходов, на которое каждый призрак 
        останется испуганным из-за того, что Пакман съел энерго-гранулу.

        Распечатайте эти переменные, чтобы увидеть и понять их значения, а затем
        комбинируйте их, чтобы создать подходящую функцию оценки.
        
        """
        
        # # Полезная информация, которую вы можете извлечь из GameState (pacman.py)
        
        # # Формируем дочернее состояниe после действия action
        # # пример схемы дочернего состояния для поля testClassic,размером 10x5 :
        # #    %%%%%
        # #    % . %
        # #    %.G.%
        # #    % . %
        # #    %. .%
        # #    %   %
        # #    %  .%
        # #    %   %
        # #    %< .%
        # #    %%%%%
        # # Здесь G - призрак, < - Пакман, . - еда, % - стены
        # successorGameState = currentGameState.generatePacmanSuccessor(action)
        # # print("succ:", successorGameState)
        
        # # Определяем координаты Пакмана  в виде кортежа (x,y)
        # # Для приведенной выше схемы newPos=(1,1)
        # newPos = successorGameState.getPacmanPosition()
              
        # # Определяем положение точек еды в виде логического массива
        # # Для приведенной выше схемы newFood будет равен:
        # # FFFFF
        # # FFTFF
        # # FTFTF
        # # FFTFF
        # # FTFTF
        # # FFFFF
        # # FFFTF
        # # FFFFF
        # # FFFTF
        # # FFFFF
        # # Здесь Т - есть еда, F - нет еды
        # newFood = successorGameState.getFood()
        # # print("newFood:", newFood)
        
        # # определяем новое состояние для призраков newGhostStates 
        # newGhostStates = successorGameState.getGhostStates()
        
        # # определяем  время испуга прираков 
        # # пример значения для newScaredTimes при 2-х призраках: [40, 40]
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        import math

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        newPos = successorGameState.getPacmanPosition()

        newFood = successorGameState.getFood()

        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        score = successorGameState.getScore()

        foodList = newFood.asList()
        if foodList:
            minFoodDist = min(
                math.sqrt((newPos[0] - fx) ** 2 + (newPos[1] - fy) ** 2)
                for fx, fy in foodList
            )
            score += 1.0 / (minFoodDist + 1e-6)
        else:
            pass

        if newGhostStates:
            ghostDists = [
                math.sqrt((newPos[0] - g.getPosition()[0]) ** 2 +
                        (newPos[1] - g.getPosition()[1]) ** 2)
                for g in newGhostStates
            ]


            dangerous = [d for d, t in zip(ghostDists, newScaredTimes) if t <= 0]
            if dangerous:
                minDangerDist = min(dangerous)
                if minDangerDist < 2:
                    score -= 1000.0
                else:
                    score -= 10.0 / (minDangerDist + 1e-6)


            scared = [d for d, t in zip(ghostDists, newScaredTimes) if t > 0]
            if scared:
                minScaredDist = min(scared)
                score += 5.0 / (minScaredDist + 1e-6)

        return score

def scoreEvaluationFunction(currentGameState):
    """
    Это функция оценки по умолчанию, она просто возвращает оценку состояния.
    Эта оценка также отображается в графическом интерфейсе Pacman.

    Эта функция оценки предназначена для использования состязательными агентами.
    (не рефлекторными агентами).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
     Вам не нужно вносить в этот класс какие-либо изменения,
     но вы можете это сделать, если хотите добавить функциональность
     ко всем вашим состязательным поисковым агентам.
     Однако, пожалуйста, ничего не удаляйте.

     Примечание: это абстрактный класс: не нужно создавать его экземпляры. 
     Он определен лишь частично и предназначен для наследования.
     Agent (game.py) - еще один абстрактный класс.
     Глубина поиска по умолчанию равна 2
     Функция оценки, используемая  по умолчанию - scoreEvaluationFunction
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Индекс Пакмана всегда равен 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Ваш минимаксный агент (задание 2)
    """

    def getAction(self, gameState):
        """
        Возвращает минимаксное действие для текущего состояния gameState,
        используя self.depth и self.evaluationFunction.

        Вот несколько вызовов методов, которые могут быть полезны при реализации
        минимаксного агента.

        gameState.getLegalActions (agentIndex):
        Возвращает список допустимых (легальных) действий для агента
        agentIndex=0 соответсвует Пакману, а для призраков agentIndex > = 1

        gameState.generateSuccessor(agentIndex, action):
        Возвращает состояние-преемник после того, как агент совершит действие action.

        gameState.getNumAgents():
        Возвращает общее количество агентов в игре.

        gameState.isWin():
        Возвращает True если состояние игры является выигрышным.

        gameState.isLose ():
        Возвращает True если состояние игры является проигрышным.
        """
        _, action = self.minimax(gameState, 0, 0)
        return action

    def minimax(self, gameState, agentIndex, depth):
        # Терминальные условия
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        numAgents = gameState.getNumAgents()
        legalActions = gameState.getLegalActions(agentIndex)

        if agentIndex == 0:  # Пакман — максимизатор
            bestValue = float('-inf')
            bestAction = None
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                # следующий агент — 1 (первый призрак), глубина та же
                value, _ = self.minimax(successor, 1, depth)
                if value > bestValue:
                    bestValue = value
                    bestAction = action
            return bestValue, bestAction
        else:  # Призрак — минимизатор
            bestValue = float('inf')
            bestAction = None
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                nextAgent = agentIndex + 1
                nextDepth = depth
                if nextAgent == numAgents:   # призраки закончились → снова Пакман
                    nextAgent = 0
                    nextDepth = depth + 1     # увеличиваем глубину только здесь!
                value, _ = self.minimax(successor, nextAgent, nextDepth)
                if value < bestValue:
                    bestValue = value
                    bestAction = action
            return bestValue, bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Ваш минимаксный агент, реализующий альфа-бета отсечение (задание 3)
    """

    def getAction(self, gameState):
        """
        Возвращает минимаксное действие, используя
        self.depth and self.evaluationFunction
        """
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
       
        _, action = self.alphaBeta(gameState, 0, 0, float('-inf'), float('inf'))
        return action
    
    def alphaBeta(self, gameState, agentIndex, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        numAgents = gameState.getNumAgents()
        legalActions = gameState.getLegalActions(agentIndex)

        if agentIndex == 0:  # max
            bestValue = float('-inf')
            bestAction = None
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value, _ = self.alphaBeta(successor, 1, depth, alpha, beta)
                if value > bestValue:
                    bestValue = value
                    bestAction = action
                alpha = max(alpha, bestValue)
                if alpha >= beta:
                    break   # ОТСЕЧЕНИЕ
            return bestValue, bestAction
        else:  # min
            bestValue = float('inf')
            bestAction = None
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                nextAgent = agentIndex + 1
                nextDepth = depth
                if nextAgent == numAgents:
                    nextAgent = 0
                    nextDepth = depth + 1
                value, _ = self.alphaBeta(successor, nextAgent, nextDepth, alpha, beta)
                if value < bestValue:
                    bestValue = value
                    bestAction = action
                beta = min(beta, bestValue)
                if alpha >= beta:
                    break   # ОТСЕЧЕНИЕ
            return bestValue, bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Ваш expectimax агент (задание 4)
    """

    def getAction(self, gameState):
        """
        Возвращает  действие Пакмана, используя expectimax поиск и
        self.depth и self.evaluationFunction

        Все призраки должны выбирать свои случайные
        допустимые действия с равной вероятностью
        """
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
      
        _, action = self.expectimax(gameState, 0, 0)
        return action
    
    def expectimax(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        numAgents = gameState.getNumAgents()
        legalActions = gameState.getLegalActions(agentIndex)

        if agentIndex == 0:  # Пакман — max
            bestValue = float('-inf')
            bestAction = None
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value, _ = self.expectimax(successor, 1, depth)
                if value > bestValue:
                    bestValue = value
                    bestAction = action
            return bestValue, bestAction
        else:  # Призрак — ожидание
            total = 0.0
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                nextAgent = agentIndex + 1
                nextDepth = depth
                if nextAgent == numAgents:
                    nextAgent = 0
                    nextDepth = depth + 1
                value, _ = self.expectimax(successor, nextAgent, nextDepth)
                total += value
            # среднее по всем действиям
            return total / len(legalActions), None

def betterEvaluationFunction(currentGameState):
    """
    Ваша усовершенствованная функция оценки (вопрос 5)

     ОПИСАНИЕ: <втавьте сюда описание Вашей функции>
    """
    
    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
   
    score = currentGameState.getScore()
    pacmanPos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodList = food.asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    # 1. Текущий счёт — базовая награда
    value = score

    # 2. Расстояние до ближайшей еды (манхэттен) — штраф
    if foodList:
        minFoodDist = min(abs(pacmanPos[0]-f[0]) + abs(pacmanPos[1]-f[1])
                          for f in foodList)
        value -= 2.0 * minFoodDist     # коэффициент подбирается

    # 3. Призраки: если scared — бонус за близость, иначе штраф за близость
    for ghost in ghostStates:
        ghostPos = ghost.getPosition()
        dist = abs(pacmanPos[0]-ghostPos[0]) + abs(pacmanPos[1]-ghostPos[1])
        if ghost.scaredTimer > 0:
            value += 5.0 / (dist + 1)   # ближе страшный призрак — выгоднее
        else:
            if dist < 2:
                value -= 100.0           # очень близко — смертельно
            else:
                value -= 1.0 / dist      # чем ближе, тем хуже

    # 4. Капсулы (энергетические гранулы) — бонус за близость
    if capsules:
        minCapDist = min(abs(pacmanPos[0]-c[0]) + abs(pacmanPos[1]-c[1])
                         for c in capsules)
        value += 3.0 / (minCapDist + 1)

    return value

# Abbreviation
better = betterEvaluationFunction
