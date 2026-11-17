class Order:
    def __init__(self, customer_name, customer_email, customer_phone,
                 address_street, address_city, address_zip,
                 item_id, item_qty, order_type):
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone = customer_phone
        self.address_street = address_street
        self.address_city = address_city
        self.address_zip = address_zip
        self.item_id = item_id
        self.item_qty = item_qty
        self.order_type = order_type
        self.status = "new"
        self.paid = False

    # Публичный метод установки статуса — хотя статус должен быть неизменяем
    def set_status(self, status):
        self.status = status

    # Публичный метод, используемый только внутри класса
    def internal_recalc(self):
        pass


class Item:
    def __init__(self, item_id, price):
        self.item_id = item_id
        self.price = price


class OrderService:
    def __init__(self):
        self.items = []
        self.orders = []

    # ------------------------------------------------------------------
    # Длинный список параметров (data clump)
    # ------------------------------------------------------------------
    def create_order(self, customer_name, customer_email, customer_phone,
                     address_street, address_city, address_zip,
                     item_id, item_qty, order_type):
        order = Order(customer_name, customer_email, customer_phone,
                      address_street, address_city, address_zip,
                      item_id, item_qty, order_type)
        self.orders.append(order)
        return order

    # ------------------------------------------------------------------
    # Смешение запроса и модификатора: возвращает сумму и помечает оплату
    # ------------------------------------------------------------------
    def get_total_and_mark_paid(self, order):
        total = self.calc(order)
        order.paid = True
        return total

    # ------------------------------------------------------------------
    # Имя метода не раскрывает назначения
    # ------------------------------------------------------------------
    def calc(self, order):
        item = self.find_item(order.item_id)   # возвращает Object
        real_item = item                       # нисходящее преобразование
        return real_item.price * order.item_qty

    # ------------------------------------------------------------------
    # Возвращает Object — клиент вынужден делать downcast
    # ------------------------------------------------------------------
    def find_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    # ------------------------------------------------------------------
    # Параметр discount можно получить из объекта клиента
    # ------------------------------------------------------------------
    def calculate_total(self, order, discount):
        return self.calc(order) - discount

    # ------------------------------------------------------------------
    # Код ошибки вместо исключения
    # ------------------------------------------------------------------
    def pay(self, order, amount):
        if amount <= 0:
            return -1   # код ошибки
        if order.paid:
            return -2   # код ошибки
        order.paid = True
        return 0