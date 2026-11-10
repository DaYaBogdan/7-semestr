##//////////////////////////////////////////////////////////////#
#|        Заметки оставил Смирнов Б.В.                          |
#|        Для лучшего понимания что я тут наваял                |
#|        Они могут быть непонятны для вас, но мне сойдут       |
##//////////////////////////////////////////////////////////////#

def fmt(s: set) -> str:
        return str(s) if s else '∅'

def fmt_plus(s: set) -> str:
    return '{' + ', '.join(sorted(s)) + '}' if s else '∅'

SUP = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")

def sup(n) -> str:
    return str(n).translate(SUP)

# Столкнулся с проблемой, что не помню как и где у меня лежат переменные, буду записывать в комментариях под переменными
class XSolver():
    
    def __init__(self, A1: list):
        # Матрица A1 для отношений >=
        self.A1 = A1
        
        # Карты X_+ и X_- для каждого xi 
        self.xPlus_all = {}
        self.xMinus_all = {}
        # Вид x*_all = {
        #    'x1' -> {},
        #    'x2' -> {'x1'},
        #    'x3' -> {'x1', 'x2'},
        #    и т.д.
        #}
        
        # Карта функции полезности U(xi)
        self.U = {}
        # Вид U = {
        #    'x1' -> 0,
        #    'x2' -> 1,
        #    'x3' -> 0.5,
        #    и т.д.
        #}
        self.Interseptions = []
        
        # Карта правил для вычисления значений U(xi)
        self.URules = [
            (lambda xPlus, xMinus: not xPlus and xMinus                                          , self.firstApply    ),
            (lambda xPlus, xMinus: xPlus and not xMinus                                          , self.secondApply   ),
            (lambda xPlus, xMinus: xPlus and xMinus and not self.hasInterseptions(xPlus, xMinus) , self.thirdApply    ),
            (lambda xPlus, xMinus: xPlus and xMinus and self.hasInterseptions(xPlus, xMinus)     , self.fourthApply   )
        ]
    
    # Функция поиска пересечений
    def hasInterseptions(self, arr1, arr2): 
        self.Interseptions = [x for x in arr1 if (x in arr2)]
        return bool(self.Interseptions)
    
    # Функция поиска U(x')
    def UXMinFromXPlus(self, target):
        try:
            UX = min([self.U[x_i] for x_i in self.xPlus_all[target]])
            return UX
        except:
            return 0
        
    # Функция поиска U(x")
    def UXMaxFromXMinus(self, target):
        try:
            UX = max([self.U[x_i] for x_i in self.xMinus_all[target]])
            return UX
        except:
            return 0
    
    # ВНИМАНИЕ TARGET ПЕРЕДАЁТСЯ КАК 'xi' НИКАКИХ ДРУГИХ ПЕРЕМЕННЫХ 
    def firstApply(self, target):
        return self.UXMinFromXPlus(target) + 1
    def secondApply(self, target):
        return self.UXMinFromXPlus(target) - 1
    def thirdApply(self, target):
        return (self.UXMinFromXPlus(target) + self.UXMaxFromXMinus(target)) / 2
    def fourthApply(self, target):
        return self.U[self.Interseptions[0]]
    
    # Нахождение всех X_+ по xi
    def findXplus(self, target: int) -> set:
        
        xPlus_indexed = set()
        
        for iRow in range(target):
            if self.A1[iRow][target]: 
                xPlus_indexed.add(f'x{iRow + 1}')
        
        return xPlus_indexed
    
    # Нахождение всех X_- по xi
    def findXMinus(self, target: int) -> set:
        
        xMinus_indexed = set()
        
        for iCol in range(target):
            if self.A1[target][iCol]:
                xMinus_indexed.add(f'x{iCol + 1}')
                
        return xMinus_indexed
    
    def findUOnX(self, target: int) -> int:
        xPlus = self.xPlus_all[f'x{target + 1}']
        xMinus = self.xMinus_all[f'x{target + 1}']
        
        for condition, action in self.URules:
            if condition(xPlus, xMinus):
                return action(f'x{target + 1}')
        return 0
    
    # Нахождение X_+ и X_- по всем xi
    def makeXmaps(self):
        for x_index in range(len(self.A1)):
            #Ищем X_+ и X_-
            self.xPlus_all[f'x{x_index + 1}'] = self.findXplus(target=x_index)
            self.xMinus_all[f'x{x_index + 1}'] = self.findXMinus(target=x_index)
            
            # Ищем U для x
            self.U[f'x{x_index + 1}'] = self.findUOnX(target=x_index)

    def printSolution(self):
        for i in range(len(self.A1)):
            k = f'x{i+1}'
            n = i
            plus  = f"X₊{sup(n)} = {fmt(self.xPlus_all[k])}"
            minus = f"X₋{sup(n)} = {fmt(self.xMinus_all[k])}"
            u     = f"U(x{sup(n + 1)}) = {self.U[k]}"
            
            print(f"{plus:<25}\t{minus:<25}\t{u}")
        
    