class Employee:
    def __init__(self, name, salary, years, country,
                 department_name, department_head, department_budget):
        self.name = name
        self.salary = salary
        self.years = years
        self.country = country
        # Поля отдела «размазаны» по сотруднику
        self.department_name = department_name
        self.department_head = department_head
        self.department_budget = department_budget

    def get_department_head_name(self):
        # Классический посредник — клиент вынужден знать о department_head
        return self.department_head

    def calculate_salary(self):
        # Расчёт зарплаты с учётом стажа и страны
        base = self.salary
        if self.years > 5:
            base *= 1.10
        elif self.years > 2:
            base *= 1.05

        if self.country == "RU":
            tax = base * 0.13
        elif self.country == "US":
            tax = base * 0.20
        else:
            tax = base * 0.25

        return base - tax

    def calculate_bonus(self):
        # Бонус зависит от бюджета отдела — а бюджет «живёт» в сотруднике
        if self.department_budget > 1_000_000:
            return self.salary * 0.15
        return self.salary * 0.05


# Клиентский код
def print_employee_report(employee):
    print(f"Employee: {employee.name}")
    print(f"Department: {employee.department_name}")
    # Прямое обращение к внутреннему полю — нарушение инкапсуляции
    print(f"Department budget: {employee.department_budget}")
    # Посредник: клиент знает, что глава отдела хранится в Employee
    print(f"Head: {employee.get_department_head_name()}")
    print(f"Salary: {employee.calculate_salary()}")
    print(f"Bonus: {employee.calculate_bonus()}")