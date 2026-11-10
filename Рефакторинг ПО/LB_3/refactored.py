# ======================================================================
# ЗАМЕНА УСЛОВНОГО ОПЕРАТОРА ПОЛИМОРФИЗМОМ (Replace Conditional with
# Polymorphism): вместо if/elif по customer.type — иерархия классов.
# ======================================================================
class CustomerType:
    def apply_discount(self, amount):
        return amount


class RegularCustomer(CustomerType):
    def apply_discount(self, amount):
        return amount


class VipCustomer(CustomerType):
    def apply_discount(self, amount):
        return amount * 0.95


class PartnerCustomer(CustomerType):
    def apply_discount(self, amount):
        return amount * 0.9


CUSTOMER_TYPES = {
    "regular": RegularCustomer,
    "vip": VipCustomer,
    "partner": PartnerCustomer,
}


# ======================================================================
# ВВЕДЕНИЕ ОБЪЕКТА NULL (Introduce Null Object): вместо многократных
# проверок customer is not None / card is not None.
# ======================================================================
class NullCustomer:
    country = None
    card = None
    promo_code = None
    type = "regular"

    def get_type(self):
        return RegularCustomer()

    def is_null(self):
        return True


class NullCard:
    level = None

    def is_null(self):
        return True


# ======================================================================
# КЛАСС PaymentCalculator после рефакторинга
# ======================================================================
class PaymentCalculator:

    def calculate(self, customer, order):
        # ДЕКОМПОЗИЦИЯ УСЛОВНОГО ОПЕРАТОРА (Decompose Conditional):
        # каждый шаг вынесен в отдельный метод с осмысленным именем.
        if customer is None:
            customer = NullCustomer()
        if customer.card is None:
            customer.card = NullCard()

        base = self._apply_card_discount(customer, order.total)
        base = self._apply_customer_type_discount(customer, base)
        total = base + self._calculate_shipping(order.total)
        return total - self._find_promo_discount(customer, order)

    # ------------------------------------------------------------------
    # ДЕКОМПОЗИЦИЯ УСЛОВНОГО ОПЕРАТОРА: условие и ветки вынесены
    # в отдельные методы.
    # ------------------------------------------------------------------
    def _apply_card_discount(self, customer, total):
        # ЗАМЕНА ВЛОЖЕННЫХ УСЛОВНЫХ ОПЕРАТОРОВ ГРАНИЧНЫМ ОПЕРАТОРОМ
        # (Replace Nested Conditional with Guard Clauses): вместо
        # "стрелки" — ранние возвраты для особых случаев.
        if customer.card.is_null():
            return total

        if customer.country is None:
            return total

        if customer.country == "RU":
            return self._ru_card_discount(customer, total)

        if customer.country == "US":
            return self._us_card_discount(total)

        return total

    # ДЕКОМПОЗИЦИЯ УСЛОВНОГО ОПЕРАТОРА + КОНСОЛИДАЦИЯ УСЛОВНОГО
    # ВЫРАЖЕНИЯ (Consolidate Conditional Expression): несколько
    # проверок объединены в одно условие.
    def _ru_card_discount(self, customer, total):
        # ВВЕДЕНИЕ ПОЯСНЯЮЩЕЙ ПЕРЕМЕННОЙ: сложное условие разбито.
        is_gold = customer.card.level == "gold"
        if total > 1000 and is_gold:
            return total * 0.8
        if total > 1000:
            return total * 0.9
        return total * 0.95

    def _us_card_discount(self, total):
        # КОНСОЛИДАЦИЯ УСЛОВНОГО ВЫРАЖЕНИЯ: два условия > 1000
        # дают одинаковый результат — объединены.
        if total > 1000:
            return total * 0.85
        return total * 0.95

    # ------------------------------------------------------------------
    # КОНСОЛИДАЦИЯ ДУБЛИРУЮЩИХСЯ УСЛОВНЫХ ФРАГМЕНТОВ (Consolidate
    # Duplicate Conditional Fragments): вместо дублирования кода
    # доставки во всех ветках — один общий вызов.
    # ------------------------------------------------------------------
    def _calculate_shipping(self, total):
        return 20 if total > 500 else 10

    # ------------------------------------------------------------------
    # ЗАМЕНА УСЛОВНОГО ОПЕРАТОРА ПОЛИМОРФИЗМОМ: вместо if/elif по
    # customer.type — вызов полиморфного метода.
    # ------------------------------------------------------------------
    def _apply_customer_type_discount(self, customer, amount):
        customer_type = CUSTOMER_TYPES.get(customer.type)
        if customer_type is None:
            raise ValueError("Unknown customer type")
        return customer_type().apply_discount(amount)

    # ------------------------------------------------------------------
    # УДАЛЕНИЕ УПРАВЛЯЮЩЕГО ФЛАГА (Remove Control Flag): вместо
    # переменной found — ранний return из цикла.
    # ------------------------------------------------------------------
    def _find_promo_discount(self, customer, order):
        if customer.promo_code is None:
            return 0.0
        for promo in order.promos:
            if promo.code == customer.promo_code:
                return promo.value
        return 0.0