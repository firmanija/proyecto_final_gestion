class Sale:
    def __init__(self, id, product, employee, quantity):
        self.id = id
        self.product = product
        self.employee = employee
        self.quantity = quantity
        self.total = self.calculate_total()

    def calculate_total(self):
        return self.product.price * self.quantity
