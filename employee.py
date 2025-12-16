class Employee:
    def __init__(self, id, name, salary):
        self.id = id
        self.name = name
        self.salary = salary
        self.commissions = 0

    def add_commission(self, amount):
        self.commissions += amount
