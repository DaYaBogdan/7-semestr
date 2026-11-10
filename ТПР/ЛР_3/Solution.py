import matplotlib.pyplot as plt
import numpy as np

class Solution:
    
    def __init__(self, range_cost:tuple, range_mileage:tuple):
        self.range_cost = range_cost
        self.range_mileage = range_mileage
        self.discrete_criteria_cost = self.discreteCriteria(self.range_cost, 25)
        self.discrete_criteria_mileage = self.discreteCriteria(self.range_mileage, 20)
        self.k1 = [1/i for i in self.discrete_criteria_cost]
        self.k2 = [1/i for i in self.discrete_criteria_mileage]
        
        n = len(self.k1)
        self.u1 = list(np.arange(n - 1, -1, -1, dtype=int))
        self.u2 = list(np.arange(n - 1, -1, -1, dtype=int))  

        self.a1 = self.b1 = self.a2 = self.b2 = None
        self.j = None

    def discreteCriteria(self, range_criteria, step):
        criteriaList = [i for i in range(range_criteria[0], range_criteria[1]+1, step)]
        return criteriaList

    def displayCurvesOfIndiffernce(self):
        """Выполнить построение кривых безразличия в критериальном пространстве,
        а также формирование дискретных оценок критериев k1 и k2"""

        self.k1.reverse()
        self.k2.reverse()
        self.u1.reverse()
        self.u2.reverse()
        k1 = np.array(self.k1)
        k2 = np.array(self.k2)
        u1 = np.array(self.u1)
        u2 = np.array(self.u2)

        n = len(k1)

        print(f"Вектор критериев (цена):\n{k1}\nСоответствующая оценка каждого критерия:\n{u1}")
        print(f"Вектор критериев (пробег):\n{k2}\nСоответствующая оценка каждого критерия:\n{u2}")

        fig, ax = plt.subplots(figsize=(10, 8))


        for i, val_k1 in enumerate(k1):
            ax.axvline(x=val_k1, color='gray', linestyle='--', alpha=0.5, zorder=1)
        for j, val_k2 in enumerate(k2):
            ax.axhline(y=val_k2, color='gray', linestyle='--', alpha=0.5, zorder=1)


        utility_levels = {}
        for i in range(n):
            for j in range(n):
                u_total = u1[i] + u2[j]
                if u_total not in utility_levels:
                    utility_levels[u_total] = []
                utility_levels[u_total].append((k1[i], k2[j]))


        sorted_levels = sorted(utility_levels.keys())
        num_levels = len(sorted_levels)
        

        if num_levels <= 10:
            cmap = plt.cm.tab10
        else:
            cmap = plt.cm.tab20
            
        colors = cmap(np.linspace(0, 1, num_levels))
        
        point_counter = 1

        for idx, u_val in enumerate(sorted_levels):
            pts = utility_levels[u_val]
            if len(pts) > 1:
                pts_sorted = sorted(pts, key=lambda x: x[0])
                x_vals = [p[0] for p in pts_sorted]
                y_vals = [p[1] for p in pts_sorted]
                
                color = colors[idx]
                
                ax.plot(x_vals, y_vals, 'o-', color=color, linewidth=2, 
                        markersize=8, zorder=3, label=f'U = {u_val}')
                
                for x, y in zip(x_vals, y_vals):
                    ax.annotate(f'$X_{{{point_counter}}}$', (x, y), 
                                textcoords="offset points", xytext=(8, 8), 
                                ha='center', fontsize=12, fontweight='bold',
                                color=color) 
                    point_counter += 1


        ax.set_xlim(k1[0] - 0.1 * (k1[-1] - k1[0]), k1[-1] + 0.1 * (k1[-1] - k1[0]))
        ax.set_ylim(k2[0] - 0.1 * (k2[-1] - k2[0]), k2[-1] + 0.1 * (k2[-1] - k2[0]))

        xticks_labels = [f'$k_1^{{{i}}}$' for i in range(len(k1))]
        yticks_labels = [f'$k_2^{{{j}}}$' for j in range(len(k2))]
        
        ax.set_xticks(k1)
        ax.set_xticklabels(xticks_labels, fontsize=12)
        ax.set_yticks(k2)
        ax.set_yticklabels(yticks_labels, fontsize=12)

        ax.set_xlabel('$K_1$ (1/цена)', fontsize=14)
        ax.set_ylabel('$K_2$ (1/пробег)', fontsize=14)
        ax.set_title('Кривые безразличия в критериальном пространстве', fontsize=16)
        

        ax.annotate('', xy=(k1[-1] + 0.15 * (k1[-1] - k1[0]), k2[0]), 
                    xytext=(k1[-1], k2[0]), arrowprops=dict(arrowstyle='->', color='black', lw=2))
        ax.annotate('', xy=(k1[0], k2[-1] + 0.15 * (k2[-1] - k2[0])), 
                    xytext=(k1[0], k2[-1]), arrowprops=dict(arrowstyle='->', color='black', lw=2))

        ax.grid(True, alpha=0.3, zorder=0)
        

        ax.legend(loc='best', fontsize=12, title="Уровень полезности")
        
        plt.tight_layout()
        plt.show()

    def additiveUFunction(self):
        return None

    def U1(self, k1):
        return self.a1*k1+self.b1*k1**2
    def U2(self, k2):
        return self.a2*k2+self.b2*k2**2

    def U(self, k1, k2):
        return self.j*self.U1(k1)+(1-self.j)*self.U2(k2)

    def displaySolution(self, k1, k2):
        UForSolutions = []
        for i in range(len(k1)):
            UForSolutions.append(self.U(k1[i], k2[i]))

        n = 4
        col_width = 22  # ширина одной колонки

        headers = [f"Решение x{i+1}" for i in range(n)]
        print(" "*10 + "".join(f"{h:<{col_width}}" for h in headers))

        rows = [
            ("Цена",    [1 / k1[i] for i in range(n)]),
            ("Пробег",  [1 / k2[i] for i in range(n)]),
            ("U1(k1)",  [f"{self.U1(k1[i]):.3f}" for i in range(n)]),
            ("U2(k2)",  [f"{self.U1(k2[i]):.3f}" for i in range(n)]),
            ("U",       [f"{UForSolutions[i]:.3f}" for i in range(n)]),
        ]

        for name, values in rows:
            print(f"{name:<10}" + "".join(f"{v:<{col_width}}" for v in values))

        return max(UForSolutions)
    
    def findJ(self, k1_i, k1_j, k2_i, k2_j):
        u1_i = self.U1(k1_i)
        u2_i = self.U2(k2_i)
        u1_j = self.U1(k1_j)
        u2_j = self.U2(k2_j)

        numerator = u2_j - u2_i
        denominator = (u1_i - u1_j) + (u2_j - u2_i)

        self.j = numerator/denominator


    def polinom(self):
        """Выполняет аппроксимацию дискретных оценок полиномами 2-го порядка
        и выводит уравнения функций, а также строит графики аппроксимации."""
        
        k1 = np.array(self.k1, dtype=float)
        A1 = np.column_stack([k1, k1**2])
        self.a1, self.b1 = np.linalg.lstsq(A1, self.u1, rcond=None)[0]

        k2 = np.array(self.k2, dtype=float)
        A2 = np.column_stack([k2, k2**2])
        self.a2, self.b2 = np.linalg.lstsq(A2, self.u2, rcond=None)[0]

        print("\n" + "="*50)
        print("АППРОКСИМИРУЮЩИЕ ФУНКЦИИ (ПОЛИНОМЫ 2-ГО ПОРЯДКА)")
        print("="*50)
        print(f"U1(k1) = {self.a1:.4f} * k1 + {self.b1:.4f} * k1^2")
        print(f"U2(k2) = {self.a2:.4f} * k2 + {self.b2:.4f} * k2^2")
        print("="*50 + "\n")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        k1_dense = np.linspace(min(k1), max(k1), 100)
        k1_dense = np.linspace(0, 0.5, 100)
        u1_dense = self.a1 * k1_dense + self.b1 * k1_dense**2
        
        ax1.scatter(k1, self.u1, color='red', s=60, zorder=3, label='Дискретные оценки')
        ax1.plot(k1_dense, u1_dense, color='blue', linewidth=2, 
                 label=f'Аппроксимация:\nU1 = {self.a1:.3f}k1 + {self.b1:.3f}k1²')
        ax1.set_xlabel('k1 (1/цена)', fontsize=12)
        ax1.set_ylabel('U1', fontsize=12)
        ax1.set_title('Аппроксимация U1(k1)', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=10)

        k2_dense = np.linspace(min(k2), max(k2), 100)
        u2_dense = self.a2 * k2_dense + self.b2 * k2_dense**2
        
        ax2.scatter(k2, self.u2, color='green', s=60, zorder=3, label='Дискретные оценки')
        ax2.plot(k2_dense, u2_dense, color='orange', linewidth=2, 
                 label=f'Аппроксимация:\nU2 = {self.a2:.3f}k2 + {self.b2:.3f}k2²')
        ax2.set_xlabel('k2 (1/пробег)', fontsize=12)
        ax2.set_ylabel('U2', fontsize=12)
        ax2.set_title('Аппроксимация U2(k2)', fontsize=14)
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10)

        plt.tight_layout()
        plt.show()

        prices = np.array([30, 50, 80, 25])
        k1_alt = 1.0 / prices
        U1_alt = self.a1 * k1_alt + self.b1 * k1_alt**2

        mileages = np.array([45, 30, 20, 55])
        k2_alt = 1.0 / mileages
        U2_alt = self.a2 * k2_alt + self.b2 * k2_alt**2
        
        print("Оценки для альтернативных решений:")
        print(f"U1_alt: {U1_alt}")
        print(f"U2_alt: {U2_alt}")

    
a = Solution((25,100), (20, 80))

print(a.displayCurvesOfIndiffernce())
a.polinom()
a.findJ(1/20, 1/40, 1/75, 1/10)
a.displaySolution([1/30, 1/50, 1/80, 1/25], [1/45, 1/30, 1/20, 1/55])

