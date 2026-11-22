class Lab2Solver:
    def __init__(self, A1: list, A2: list):
        
        if not A2: 
            A2 = self.make_equal_matrix(A1)
            A1 = self.make_prefference_matrix(A1)

        self.A1 = A1 
        self.A2 = A2  
        
        self.n = len(self.A2) 
        
        self.R = {}
        self.K = {}
        self.U_k = {}
        self.U_x = {}          # <-- добавить     

    def make_prefference_matrix(self, A1: list):
        return [[1 if A1[i][j] != A1[j][i] and A1[i][j] == 1 else 0 for j in range(len(A1))] for i in range(len(A1))]
    
    def make_equal_matrix(self, A1: list):
        return [[1 if A1[i][j] == A1[j][i] and A1[i][j] == 1 else 0 for j in range(len(A1))] for i in range(len(A1))]
    
    def step1_find_equivalence_classes(self):
        for i in range(self.n):
            self.R[f'x{i+1}'] = set()
            for j in range(self.n):
                if self.A2[i][j] == 1:
                    self.R[f'x{i+1}'].add(f'x{j+1}')

    def step2_find_unique_classes(self):
        unique_sets = []
        for i in range(self.n):
            current_R = self.R[f'x{i+1}']
            if current_R not in unique_sets:
                unique_sets.append(current_R)
                
        for idx, k_set in enumerate(unique_sets):
            self.K[f'K_{idx+1}'] = k_set

    def step3_calculate_U_for_classes(self):
        num_classes = len(self.K)
        
        class_A1 = [[0] * num_classes for _ in range(num_classes)]
        
        for i in range(self.n):
            for j in range(self.n):
                if self.A1[i][j] == 1:
                    class_i = None
                    class_j = None
                    for k_idx, (k_name, k_set) in enumerate(self.K.items()):
                        if f'x{i+1}' in k_set: class_i = k_idx
                        if f'x{j+1}' in k_set: class_j = k_idx
                            
                    if class_i is not None and class_j is not None and class_i != class_j:
                        class_A1[class_i][class_j] = 1

        print("\n--- Матрица предпочтений между классами (Class_A1) ---")
        for row in class_A1:
            print(row)
        print("-" * 50)
        
        self.U_k['K_1'] = 0

                # --- Расчёт U(K) на основе классов полезности ---
        # U(K_1) = 0 (задано выше).
        # Правила:
        #   1) K_l > K_h  =>  U(K_l) = U(K_h) + 1
        #   2) K_h > K_l  =>  U(K_l) = U(K_h) - 1
        #   3) K_h > K_l и K_l > K_r  =>  U(K_l) = (U(K_h) + U(K_r)) / 2
        #
        # class_A1[a][b] == 1  означает  K_a > K_b  (a лучше b).

        def strictly_better(a, b):
            return class_A1[a][b] == 1 and class_A1[b][a] == 0

        # Итеративно досчитываем, пока есть прогресс
        changed = True
        while changed:
            changed = False
            for l in range(num_classes):
                k_key = f'K_{l + 1}'
                if self.U_k.get(k_key) is not None:
                    continue

                # Кандидаты: h — лучше l (K_h > K_l), r — хуже l (K_l > K_r)
                h_cands = [h for h in range(num_classes)
                           if h != l and strictly_better(h, l)]
                r_cands = [r for r in range(num_classes)
                           if r != l and strictly_better(l, r)]

                # Правило 3: «сэндвич» K_h > K_l > K_r, оба соседа известны
                if h_cands and r_cands:
                    done = False
                    for h in h_cands:
                        for r in r_cands:
                            u_h = self.U_k.get(f'K_{h + 1}')
                            u_r = self.U_k.get(f'K_{r + 1}')
                            if u_h is not None and u_r is not None:
                                self.U_k[k_key] = (u_h + u_r) / 2
                                done = True
                                break
                        if done:
                            break
                    if done:
                        changed = True
                        continue

                # Правило 1: K_l > K_h  =>  U(K_l) = U(K_h) + 1
                # (есть r, которого l лучше, и U(K_r) известен)
                if r_cands:
                    for r in r_cands:
                        u_r = self.U_k.get(f'K_{r + 1}')
                        if u_r is not None:
                            self.U_k[k_key] = u_r + 1
                            changed = True
                            break
                    if self.U_k.get(k_key) is not None:
                        continue

                # Правило 2: K_h > K_l  =>  U(K_l) = U(K_h) - 1
                # (есть h, который лучше l, и U(K_h) известен)
                if h_cands:
                    for h in h_cands:
                        u_h = self.U_k.get(f'K_{h + 1}')
                        if u_h is not None:
                            self.U_k[k_key] = u_h - 1
                            changed = True
                            break
                    if self.U_k.get(k_key) is not None:
                        continue

        print("\n--- Полезности классов U(K_j) ---")
        for k_idx in range(1, num_classes + 1):
            print(f"U(K_{k_idx}) = {self.U_k.get(f'K_{k_idx}')}")
        print("-" * 50)
                    
    def step4_calculate_U_for_solutions(self):
        for k_key, k_set in self.K.items():
            u_val = self.U_k[k_key]
            for x_i in k_set:
                self.U_x[x_i] = u_val

    def print_results(self):
        print(f"\n--- 0. Матрицы A1 и A2 ---")
        print("A1:")
        for i in range(len(self.A1)): print(f"x{i + 1}:{self.A1[i]}")
        print()
        print("A2:")
        for i in range(len(self.A2)): print(f"x{i + 1}:{self.A2[i]}")
        print(f"\n--- 1. Классы эквивалентности R(x_i) ---")
        for k, v in self.R.items():
            print(f"{k}: {{ {', '.join(sorted(v))} }}")
            
        print(f"\n--- 2. Уникальные классы X/~ ---")
        for k, v in self.K.items():
            print(f"{k}: {{ {', '.join(sorted(v))} }}")
            
        print(f"\n--- 3. Полезность классов U(K_j) ---")
        for k, v in self.U_k.items():
            print(f"U({k}) = {v}")
            
        print(f"\n--- 4. Полезность решений U(x_i) ---")
        for k in sorted(self.U_x.keys(), key=lambda x: int(x[1:])):
            print(f"U({k}) = {self.U_x[k]}")
            
        print(f"\n--- 5. Поиск эффективного решения ---")
        max_U = max(self.U_x.values())
        best_x = [x for x, u in self.U_x.items() if u == max_U]
        print(f"Максимальная полезность: U = {max_U}")
        print(f"Эффективное решение: {best_x}")

# A1 = [
#     [0, 0, 0, 0, 0, 0, 0], # x1
#     [1, 0, 1, 0, 0, 1, 0], # x2
#     [0, 0, 0, 0, 0, 0, 0], # x3
#     [0, 1, 0, 0, 1, 0, 0], # x4
#     [1, 0, 1, 0, 0, 1, 0], # x5
#     [0, 0, 0, 0, 0, 0, 0], # x6
#     [0, 1, 0, 0, 1, 0, 0]  # x7
# ]

# A2 = [
#     [1, 0, 1, 0, 0, 1, 0], # x1
#     [0, 1, 0, 0, 1, 0, 0], # x2
#     [1, 0, 1, 0, 0, 1, 0], # x3
#     [0, 0, 0, 1, 0, 0, 1], # x4
#     [0, 1, 0, 0, 1, 0, 0], # x5
#     [1, 0, 1, 0, 0, 1, 0], # x6
#     [0, 0, 0, 1, 0, 0, 1]  # x7
# ]

# solver = Lab2Solver(A1, A2)
# solver.step1_find_equivalence_classes()
# solver.step2_find_unique_classes()
# solver.step3_calculate_U_for_classes()
# solver.step4_calculate_U_for_solutions()
# solver.print_results()

# A1 = [[1, 1, 0, 0, 0],
#       [1, 1, 0, 0, 0],
#       [0, 1, 1, 0, 1],
#       [0, 0, 0, 1, 1],
#       [0, 0, 1, 0, 1]]

# solver = Lab2Solver(A1, None)
# solver.step1_find_equivalence_classes()
# solver.step2_find_unique_classes()
# solver.step3_calculate_U_for_classes()
# solver.step4_calculate_U_for_solutions()
# solver.print_results()

A1 = [[1, 0, 0, 1, 0],
      [0, 1, 0, 0, 1],
      [0, 1, 1, 1, 0],
      [0, 0, 1, 1, 0],
      [0, 1, 0, 0, 1]]

solver = Lab2Solver(A1, None)
solver.step1_find_equivalence_classes()
solver.step2_find_unique_classes()
solver.step3_calculate_U_for_classes()
solver.step4_calculate_U_for_solutions()
solver.print_results()