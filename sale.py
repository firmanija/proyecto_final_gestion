from datetime import datetime


class Sale:
    def __init__(
        self,
        id,
        product,
        employee,
        quantity,
        payment_method,
        customer_id=None,
        customer_name=None,
        date=None
    ):
        self.id = id
        self.product = product
        self.employee = employee
        self.quantity = quantity
        self.payment_method = payment_method
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.date = date if date else datetime.now()
        self.total = self.calculate_total()

    def calculate_total(self):
        return self.product.price * self.quantity

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product.id,
            "product_name": self.product.name,
            "employee": self.employee,
            "quantity": self.quantity,
            "payment_method": self.payment_method,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "date": self.date.isoformat(),
            "total": self.total,
        }

    @classmethod
    def from_dict(cls, data, product):
        date_value = data.get("date")
        parsed_date = datetime.fromisoformat(date_value) if date_value else datetime.now()

        return cls(
            id=data["id"],
            product=product,
            employee=data["employee"],
            quantity=data["quantity"],
            payment_method=data["payment_method"],
            customer_id=data.get("customer_id"),
            customer_name=data.get("customer_name"),
            date=parsed_date,
        )


class Sales:
    def __init__(self):
        self.sales_data = []

    def record_sale(
        self,
        id,
        product,
        employee,
        quantity,
        payment_method,
        customer_id=None,
        customer_name=None
    ):
        sale = Sale(
            id=id,
            product=product,
            employee=employee,
            quantity=quantity,
            payment_method=payment_method,
            customer_id=customer_id,
            customer_name=customer_name,
        )

        self.sales_data.append(sale)
        return sale

    def list_sales(self):
        if not self.sales_data:
            print("No sales registered.")
            return

        print("\n--- SALES HISTORY ---")

        for sale in self.sales_data:
            customer_display = sale.customer_name if sale.customer_name else "Walk-in"

            print(
                f"ID: {sale.id} | "
                f"Date: {sale.date.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Product: {sale.product.name} | "
                f"Qty: {sale.quantity} | "
                f"Customer: {customer_display} | "
                f"Employee: {sale.employee} | "
                f"Payment: {sale.payment_method} | "
                f"Total: ${sale.total:.2f}"
            )

    def get_total_revenue(self):
        return sum(sale.total for sale in self.sales_data)

    def get_sales_count(self):
        return len(self.sales_data)

    def get_next_sale_id(self):
        if not self.sales_data:
            return 1
        return max(sale.id for sale in self.sales_data) + 1

    def to_dict_list(self):
        return [sale.to_dict() for sale in self.sales_data]

    def load_from_dict_list(self, sales_data, inventory):
        self.sales_data = []

        for item in sales_data:
            product_id = item.get("product_id")
            product = inventory.get_product(product_id)

            if product:
                sale = Sale.from_dict(item, product)
                self.sales_data.append(sale)