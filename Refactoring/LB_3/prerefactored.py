class PaymentCalculator:
    def calculate(self, customer, order):
        # --- управляющий флаг в цикле поиска скидки ---
        discount = 0.0
        found = False
        for promo in order.promos:
            if not found:
                if promo.code == customer.promo_code:
                    discount = promo.value
                    found = True
                else:
                    continue

        # --- глубоко вложенные условия (arrow anti-pattern) ---
        result = 0.0
        if customer is not None:
            if customer.card is not None:
                if customer.country == "RU":
                    if order.total > 1000:
                        if customer.card.level == "gold":
                            result = order.total * 0.8
                        else:
                            result = order.total * 0.9
                    else:
                        result = order.total * 0.95
                elif customer.country == "US":
                    if order.total > 1000:
                        result = order.total * 0.85
                    else:
                        result = order.total * 0.95
                else:
                    result = order.total
            else:
                result = order.total
        else:
            result = order.total

        # --- дублирование одинакового кода во всех ветках ---
        if order.total > 500:
            result += 20  # доставка
        else:
            result += 10  # доставка

        # --- switch-подобная логика по типу клиента ---
        if customer is not None:
            if customer.type == "regular":
                result = result
            elif customer.type == "vip":
                result = result * 0.95
            elif customer.type == "partner":
                result = result * 0.9
            else:
                raise ValueError("Unknown customer type")

        return result - discount