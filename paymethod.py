class PaymentMethod:
    def __init__(self, method_type):
        self.method_type = method_type
        self.total_received = 0

    def record_payment(self, amount):
        self.total_received += amount
