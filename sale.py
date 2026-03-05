class Sale:
    def __init__(self, id, product, employee, quantity, payment_method):
        self.id = id
        self.product = product
        self.employee = employee
        self.quantity = quantity
        self.payment_method = payment_method
        self.total = self.calculate_total()

    def calculate_total(self):
        return self.product.price * self.quantity

class Sales:
    def __init__(self):
        self.sales_data = []

    def record_sale(self, id, product, employee, quantity, payment_method):
        """Record a sale using the specified payment method."""
        sale = Sale(id, product, employee, quantity, payment_method)
        self.sales_data.append(sale)