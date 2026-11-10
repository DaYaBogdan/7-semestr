class Lab2Solver:
    def __init__(self, A1: list, A2: list):
        self.A1 = A1  # Исходная матрица предпочтений (7x7)
        self.A2 = A2  # Исходная матрица эквивалентности (7x7)
        
        self.n = len(self.A2) 
        
        self.R = {}          
        self.Kappa = {}      
        self.U_kappa = {}    
        self.U_x = {}        
        
    def step1_find_equivalence_classes(self):
        """Пункт 2: Формирование R(x_i) на основе A2"""
        for i in range(self.n):
            self.R[f'x{i+1}'] = set()
            for j in range(self.n):
                if self.A2[i][j] == 1:
                    self.R[f'x{i+1}'].add(f'x{j+1}')

    def step2_find_unique_classes(self):
        """Пункт 3: Исключение повторяющихся, формирование X/~"""
        unique_sets = []
        for i in range(self.n):
            current_R = self.R[f'x{i+1}']
            if current_R not in unique_sets:
                unique_sets.append(current_R)
                
        for idx, k_set in enumerate(unique_sets):
            self.Kappa[f'K_{idx+1}'] = k_set

    def step3_calculate_U_for_classes(self):
        """Пункт 4: Упорядочивание классов и вычисление U(K_j)"""
        num_classes = len(self.Kappa)
        
        # 1. Формируем матрицу предпочтений для классов на основе исходной 7x7 A1
        class_A1 = [[0] * num_classes for _ in range(num_classes)]
        
        for i in range(self.n):
            for j in range(self.n):
                if self.A1[i][j] == 1:
                    class_i = None
                    class_j = None
                    for k_idx, (k_name, k_set) in enumerate(self.Kappa.items()):
                        if f'x{i+1}' in k_set: class_i = k_idx
                        if f'x{j+1}' in k_set: class_j = k_idx
                            
                    if class_i is not None and class_j is not None and class_i != class_j:
                        class_A1[class_i][class_j] = 1

        print("\n--- Матрица предпочтений между классами (Class_A1) ---")
        for row in class_A1:
            print(row)
        print("-" * 50)

        # 2. Ищем X_+ и X_- для классов
        xPlus_all = {}
        xMinus_all = {}
        
        for i in range(num_classes):
            k_key = f'K_{i+1}'
            xPlus_all[k_key] = set()
            xMinus_all[k_key] = set()
            
            for j in range(num_classes):
                # Строго по теории из картинок
                if j < i and class_A1[j][i] == 1:
                    xPlus_all[k_key].add(f'K_{j+1}')
                if j < i and class_A1[i][j] == 1:
                    xMinus_all[k_key].add(f'K_{j+1}')
                    
        print(f"--- X_+ и X_- для классов ---")
        for i in range(num_classes):
            k = f'K_{i+1}'
            print(f"{k}: X_+ = {xPlus_all[k] if xPlus_all[k] else '∅'}, X_- = {xMinus_all[k] if xMinus_all[k] else '∅'}")

        # 3. Начальные условия
        self.U_kappa['K_1'] = 0
        if num_classes > 1:
            self.U_kappa[f'K_{num_classes}'] = 1

        # 4. Вычисление U по правилам
        for i in range(1, num_classes - 1):
            k_key = f'K_{i+1}'
            xp = xPlus_all[k_key]
            xm = xMinus_all[k_key]
            
            def get_min_xp():
                return min([self.U_kappa[k] for k in xp]) if xp else 0
                
            def get_max_xm():
                return max([self.U_kappa[k] for k in xm]) if xm else 0

            if not xp and xm:       # Случай 1
                self.U_kappa[k_key] = get_max_xm() + 1
            elif xp and not xm:     # Случай 2
                self.U_kappa[k_key] = get_min_xp() - 1
            elif xp and xm:
                intersection = xp & xm
                if not intersection: # Случай 3
                    self.U_kappa[k_key] = (get_min_xp() + get_max_xm()) / 2
                else:                # Случай 4
                    x_star = next(iter(intersection))
                    self.U_kappa[k_key] = self.U_kappa[x_star]
                    
    def step4_calculate_U_for_solutions(self):
        """Пункт 5: Инициализация U(x_i) значениями U(K_j)"""
        for k_key, k_set in self.Kappa.items():
            u_val = self.U_kappa[k_key]
            for x_i in k_set:
                self.U_x[x_i] = u_val

    def print_results(self):
        """Пункт 6: Вывод результатов"""
        print(f"\n--- 1. Классы эквивалентности R(x_i) ---")
        for k, v in self.R.items():
            print(f"{k}: {{ {', '.join(sorted(v))} }}")
            
        print(f"\n--- 2. Уникальные классы X/~ ---")
        for k, v in self.Kappa.items():
            print(f"{k}: {{ {', '.join(sorted(v))} }}")
            
        print(f"\n--- 3. Полезность классов U(K_j) ---")
        for k, v in self.U_kappa.items():
            print(f"U({k}) = {v}")
            
        print(f"\n--- 4. Полезность решений U(x_i) ---")
        for k in sorted(self.U_x.keys(), key=lambda x: int(x[1:])):
            print(f"U({k}) = {self.U_x[k]}")
            
        print(f"\n--- 5. Поиск эффективного решения ---")
        max_U = max(self.U_x.values())
        best_x = [x for x, u in self.U_x.items() if u == max_U]
        print(f"Максимальная полезность: U = {max_U}")
        print(f"Эффективное решение: {best_x}")



# --- ИНИЦИАЛИЗАЦИЯ И ЗАПУСК ---

A1 = [
    [0, 0, 0, 0, 0, 0, 0], # x1
    [1, 0, 1, 0, 0, 1, 0], # x2
    [0, 0, 0, 0, 0, 0, 0], # x3
    [0, 1, 0, 0, 1, 0, 0], # x4
    [1, 0, 1, 0, 0, 1, 0], # x5
    [0, 0, 0, 0, 0, 0, 0], # x6
    [0, 1, 0, 0, 1, 0, 0]  # x7
]

A2 = [
    [1, 0, 1, 0, 0, 1, 0], # x1
    [0, 1, 0, 0, 1, 0, 0], # x2
    [1, 0, 1, 0, 0, 1, 0], # x3
    [0, 0, 0, 1, 0, 0, 1], # x4
    [0, 1, 0, 0, 1, 0, 0], # x5
    [1, 0, 1, 0, 0, 1, 0], # x6
    [0, 0, 0, 1, 0, 0, 1]  # x7
]

# Запуск
solver = Lab2Solver(A1, A2)
solver.step1_find_equivalence_classes()
solver.step2_find_unique_classes()
solver.step3_calculate_U_for_classes()
solver.step4_calculate_U_for_solutions()
solver.print_results()