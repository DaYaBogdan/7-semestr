# ======================================================================
# ВЫДЕЛЕНИЕ КЛАССА (Extract Class): Department
# Поля department_name, department_head, department_budget перенесены
# из Employee в отдельный класс Department.
# ======================================================================
class Department:
    def __init__(self, name, head, budget):
        self.name = name
        self.head = head
        self.budget = budget

    # ПЕРЕМЕЩЕНИЕ МЕТОДА (Move Method): логика бонуса зависит от бюджета
    # отдела, поэтому метод перемещён в Department.
    def calculate_bonus(self, salary):
        if self.budget > 1_000_000:
            return salary * 0.15
        return salary * 0.05

    # СОКРЫТИЕ ДЕЛЕГИРОВАНИЯ (Hide Delegate): клиенту не нужно знать,
    # что глава отдела — это поле head; он спрашивает у Department.
    def get_head_name(self):
        return self.head


# ======================================================================
# ВВЕДЕНИЕ ЛОКАЛЬНОГО РАСШИРЕНИЯ (Introduce Local Extension):
# класс TaxCalculator расширяет поведение, не трогая Employee.
# ======================================================================
class TaxCalculator:
    RATES = {
        "RU": 0.13,
        "US": 0.20,
    }
    DEFAULT_RATE = 0.25

    @classmethod
    def calculate(cls, amount, country):
        rate = cls.RATES.get(country, cls.DEFAULT_RATE)
        return amount - amount * rate


# ======================================================================
# ВВЕДЕНИЕ ВНЕШНЕГО МЕТОДА (Introduce Foreign Method):
# расширение для стороннего класса, который нельзя модифицировать.
# ======================================================================
def is_senior_employee(employee):
    """Внешний метод: должен находиться в Employee, но класс закрыт."""
    return employee.years > 5


# ======================================================================
# КЛАСС Employee после рефакторинга
# ======================================================================
class Employee:
    def __init__(self, name, salary, years, country, department):
        self.name = name
        self.salary = salary
        self.years = years
        self.country = country
        # Ссылка на отдел вместо трёх «размазанных» полей
        self._department = department

    # СОКРЫТИЕ ДЕЛЕГИРОВАНИЯ: клиенту не нужно знать о _department,
    # чтобы узнать главу отдела — Employee скрывает делегирование.
    def get_department_head_name(self):
        return self._department.get_head_name()

    # ПЕРЕМЕЩЕНИЕ МЕТОДА: расчёт бонуса делегируется в Department,
    # а Employee лишь предоставляет salary. Это устраняет зависимость
    # Employee от бюджета отдела.
    def calculate_bonus(self):
        return self._department.calculate_bonus(self.salary)

    # ЗАМЕНА ВРЕМЕННОЙ ПЕРЕМЕННОЙ ВЫЗОВОМ МЕТОДА:
    # расчёт налога вынесен в TaxCalculator (введение локального расширения).
    def calculate_salary(self):
        base = self._apply_seniority_bonus()
        return TaxCalculator.calculate(base, self.country)

    def _apply_seniority_bonus(self):
        if self.years > 5:
            return self.salary * 1.10
        if self.years > 2:
            return self.salary * 1.05
        return self.salary


# ======================================================================
# УДАЛЕНИЕ ПОСРЕДНИКА (Remove Middle Man) в клиентском коде:
# вместо employee.get_department_head_name() клиент, которому нужен
# весь отдел, обращается к department напрямую.
# ======================================================================
def print_employee_report(employee):
    dept = employee._department          # прямой доступ к делегату
    print(f"Employee: {employee.name}")
    print(f"Department: {dept.name}")
    print(f"Department budget: {dept.budget}")
    print(f"Head: {dept.get_head_name()}")
    print(f"Salary: {employee.calculate_salary()}")
    print(f"Bonus: {employee.calculate_bonus()}")
    print(f"Senior: {is_senior_employee(employee)}")