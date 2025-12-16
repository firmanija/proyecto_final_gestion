class Product:
    def __init__(self, id, name, description, price, stock):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    def add_stock(self, quantity):
        self.stock += quantity

    def remove_stock(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
        else:
            print("Not enough stock.")
