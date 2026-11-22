import unittest
from models import Item, Customer
from prerefactored import OrderProcessor as OldProcessor
from refactored import OrderProcessor as NewProcessor

class TestRefactoringEquivalence(unittest.TestCase):
    def setUp(self):
        self.old_proc = OldProcessor()
        self.new_proc = NewProcessor()

        self.customers = [
            Customer("Иван", "RU", 5),    # VIP, лояльный
            Customer("John", "US", 1),    # Не VIP, не лояльный
            Customer("Hans", "DE", 10),   # Неизвестная страна
        ]

        self.item_sets = [
            [Item(price=2000, quantity=1)], # 2000
            [Item(price=100, quantity=2)],  # 200
        ]

    def test_equivalence(self):
        print("\n--- Сравнение старого и нового кода ---")
        for customer in self.customers:
            for items in self.item_sets:
                for is_vip in [True, False]:
                    old_receipt = self.old_proc.process_order(items, customer, is_vip)
                    new_receipt = self.new_proc.process_order(items, customer, is_vip)
                    
                    self.assertEqual(old_receipt, new_receipt, 
                        f"Различия для клиента {customer.name} (VIP={is_vip})!")
                    
                    print(f"[OK] Клиент: {customer.name}, VIP: {is_vip}, Сумма: {items[0].price * items[0].quantity}")

        print("--- Все тесты пройдены. Поведение идентично! ---")

if __name__ == "__main__":
    unittest.main(verbosity=2)