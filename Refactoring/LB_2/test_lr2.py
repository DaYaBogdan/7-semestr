import unittest
from prerefactored import Employee as OldEmployee
from prerefactored import print_employee_report as old_report
from refactored import Employee as NewEmployee, Department, print_employee_report as new_report

class TestLR2Refactoring(unittest.TestCase):
    def setUp(self):
       
        self.case1 = {
            "name": "Иван", "salary": 100000, "years": 6, "country": "RU",
            "dept_name": "IT", "dept_head": "Петров", "dept_budget": 2000000
        }

        self.case2 = {
            "name": "John", "salary": 50000, "years": 1, "country": "US",
            "dept_name": "HR", "dept_head": "Smith", "dept_budget": 500000
        }

    def test_equivalence(self):
        print("\n--- Сравнение старого и нового кода (ЛР2) ---")
        
        
        old_emp1 = OldEmployee(
            self.case1["name"], self.case1["salary"], self.case1["years"], self.case1["country"],
            self.case1["dept_name"], self.case1["dept_head"], self.case1["dept_budget"]
        )
        new_dept1 = Department(self.case1["dept_name"], self.case1["dept_head"], self.case1["dept_budget"])
        new_emp1 = NewEmployee(
            self.case1["name"], self.case1["salary"], self.case1["years"], self.case1["country"], new_dept1
        )
        
        self.assertAlmostEqual(old_emp1.calculate_salary(), new_emp1.calculate_salary(), places=2, msg="Зарплата не совпала (case1)")
        self.assertAlmostEqual(old_emp1.calculate_bonus(), new_emp1.calculate_bonus(), places=2, msg="Бонус не совпал (case1)")
        self.assertEqual(old_emp1.get_department_head_name(), new_emp1.get_department_head_name(), "Глава отдела не совпал")
        print(f"[OK] Case 1 ({self.case1['name']}): Зарплата={new_emp1.calculate_salary():.2f}, Бонус={new_emp1.calculate_bonus():.2f}")

        old_emp2 = OldEmployee(
            self.case2["name"], self.case2["salary"], self.case2["years"], self.case2["country"],
            self.case2["dept_name"], self.case2["dept_head"], self.case2["dept_budget"]
        )
        new_dept2 = Department(self.case2["dept_name"], self.case2["dept_head"], self.case2["dept_budget"])
        new_emp2 = NewEmployee(
            self.case2["name"], self.case2["salary"], self.case2["years"], self.case2["country"], new_dept2
        )

        self.assertAlmostEqual(old_emp2.calculate_salary(), new_emp2.calculate_salary(), places=2, msg="Зарплата не совпала (case2)")
        self.assertAlmostEqual(old_emp2.calculate_bonus(), new_emp2.calculate_bonus(), places=2, msg="Бонус не совпал (case2)")
        print(f"[OK] Case 2 ({self.case2['name']}): Зарплата={new_emp2.calculate_salary():.2f}, Бонус={new_emp2.calculate_bonus():.2f}")

        print("\n--- Вывод отчета НОВОГО кода ---")
        new_report(new_emp1)
        
        print("--- Все тесты ЛР2 пройдены успешно! ---")

if __name__ == "__main__":
    unittest.main(verbosity=2)