class OrderProcessor:
    def process_order(self, items, customer, is_vip):
        
        subtotal = 0.0
        for item in items:
            subtotal += item.price * item.quantity

        discount = 0.0
        if is_vip and customer.years > 3:
            if subtotal > 1000:
                discount = subtotal * 0.2
            else:
                discount = subtotal * 0.1
        else:
            if subtotal > 1000:
                discount = subtotal * 0.05

        discounted = subtotal - discount

        if customer.country == "RU":
            tax = discounted * 0.18
        elif customer.country == "US":
            tax = discounted * 0.1
        else:
            tax = discounted * 0.2

        total = discounted + tax

        result = "Order for " + customer.name + "\n"
        result += "Subtotal: " + str(subtotal) + "\n"
        result += "Discount: " + str(discount) + "\n"
        result += "Tax: " + str(tax) + "\n"
        result += "Total: " + str(total) + "\n"

        if total > 5000:
            result += "Status: VIP order\n"
        else:
            result += "Status: Regular order\n"

        return result