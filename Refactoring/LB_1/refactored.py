class OrderProcessor:
    # --- ВЫДЕЛЕНИЕ КОНСТАНТ ---
    # Магические числа заменены именованными константами класса.
    # Это улучшает читаемость и упрощает изменение порогов.
    VIP_DISCOUNT_HIGH = 0.20
    VIP_DISCOUNT_NORMAL = 0.10
    REGULAR_DISCOUNT_HIGH = 0.05
    HIGH_SUBTOTAL_THRESHOLD = 1000.0
    VIP_TOTAL_THRESHOLD = 5000.0
    LOYAL_CUSTOMER_YEARS = 3

    TAX_RATES = {
        "RU": 0.18,
        "US": 0.10,
    }
    DEFAULT_TAX_RATE = 0.20

    def process_order(self, items, customer, is_vip):
        """
        Основной метод теперь читается как последовательность шагов:
        подытог -> скидка -> налог -> чек.
        """
        # ВЫДЕЛЕНИЕ МЕТОДА + ЗАМЕНА ВРЕМЕННОЙ ПЕРЕМЕННОЙ ВЫЗОВОМ МЕТОДА
        subtotal = self._calculate_subtotal(items)

        # ВЫДЕЛЕНИЕ МЕТОДА: вся логика скидки скрыта в _calculate_discount
        discount = self._calculate_discount(customer, is_vip, subtotal)

        # ВСТРАИВАНИЕ ВРЕМЕННОЙ ПЕРЕМЕННОЙ:
        # переменная discounted использовалась только один раз,
        # поэтому она встроена прямо в вызов _calculate_tax.
        tax = self._calculate_tax(customer, subtotal - discount)

        total = subtotal - discount + tax

        # ВЫДЕЛЕНИЕ МЕТОДА: формирование чека вынесено отдельно
        return self._build_receipt(customer, subtotal, discount, tax, total)

    # ------------------------------------------------------------------
    # ВЫДЕЛЕНИЕ МЕТОДА: расчёт подытога
    # ------------------------------------------------------------------
    def _calculate_subtotal(self, items):
        result = 0.0
        for item in items:
            result += item.price * item.quantity
        return result

    # ------------------------------------------------------------------
    # ВЫДЕЛЕНИЕ МЕТОДА + ВВЕДЕНИЕ ПОЯСНЯЮЩИХ ПЕРЕМЕННЫХ
    # ------------------------------------------------------------------
    def _calculate_discount(self, customer, is_vip, subtotal):
        # ВВЕДЕНИЕ ПОЯСНЯЮЩЕЙ ПЕРЕМЕННОЙ: логическое выражение вынесено
        # в отдельный метод, чтобы условие читалось как фраза.
        if is_vip and self._is_loyal_customer(customer):
            # ЗАМЕЩЕНИЕ АЛГОРИТМА: вместо вложенного if/else
            # используем тернарное выражение с поясняющей проверкой.
            rate = (self.VIP_DISCOUNT_HIGH
                    if self._is_high_subtotal(subtotal)
                    else self.VIP_DISCOUNT_NORMAL)
            return subtotal * rate

        # ВЫДЕЛЕНИЕ МЕТОДА: проверка порога вынесена в _is_high_subtotal
        if self._is_high_subtotal(subtotal):
            return subtotal * self.REGULAR_DISCOUNT_HIGH

        return 0.0

    # ------------------------------------------------------------------
    # ВВЕДЕНИЕ ПОЯСНЯЮЩЕЙ ПЕРЕМЕННОЙ (в виде метода-предиката)
    # ------------------------------------------------------------------
    def _is_loyal_customer(self, customer):
        """Поясняет смысл условия customer.years > 3."""
        return customer.years > self.LOYAL_CUSTOMER_YEARS

    def _is_high_subtotal(self, subtotal):
        """Поясняет смысл условия subtotal > 1000."""
        return subtotal > self.HIGH_SUBTOTAL_THRESHOLD

    # ------------------------------------------------------------------
    # ВЫДЕЛЕНИЕ МЕТОДА + ЗАМЕЩЕНИЕ АЛГОРИТМА
    # ------------------------------------------------------------------
    def _calculate_tax(self, customer, amount):
        # ЗАМЕЩЕНИЕ АЛГОРИТМА: вместо цепочки if/elif/else
        # используем словарь ставок — проще расширять.
        rate = self.TAX_RATES.get(customer.country, self.DEFAULT_TAX_RATE)
        return amount * rate

    # ------------------------------------------------------------------
    # ВЫДЕЛЕНИЕ МЕТОДА: формирование чека
    # ------------------------------------------------------------------
    def _build_receipt(self, customer, subtotal, discount, tax, total):
        # ЗАМЕЩЕНИЕ АЛГОРИТМА: конкатенация строк заменена на join списка —
        # это эффективнее и читается как таблица.
        lines = [
            f"Order for {customer.name}",
            f"Subtotal: {subtotal}",
            f"Discount: {discount}",
            f"Tax: {tax}",
            f"Total: {total}",
            f"Status: {self._get_status(total)}",
        ]
        return "\n".join(lines) + "\n"

    # ------------------------------------------------------------------
    # ВЫДЕЛЕНИЕ МЕТОДА: определение статуса заказа
    # ------------------------------------------------------------------
    def _get_status(self, total):
        # ЗАМЕЩЕНИЕ АЛГОРИТМА: вместо if/else — тернарное выражение
        return "VIP order" if total > self.VIP_TOTAL_THRESHOLD else "Regular order"