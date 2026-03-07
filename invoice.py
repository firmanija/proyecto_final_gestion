from datetime import datetime


class Invoice:
    def __init__(
        self,
        id,
        sale_id,
        customer_id,
        customer_name,
        product_name,
        quantity,
        payment_method,
        total,
        date=None
    ):
        self.id = id
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.product_name = product_name
        self.quantity = quantity
        self.payment_method = payment_method
        self.total = total
        self.date = date if date else datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "sale_id": self.sale_id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "payment_method": self.payment_method,
            "total": self.total,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        date_value = data.get("date")
        parsed_date = datetime.fromisoformat(date_value) if date_value else datetime.now()

        return cls(
            id=data["id"],
            sale_id=data["sale_id"],
            customer_id=data.get("customer_id"),
            customer_name=data.get("customer_name"),
            product_name=data["product_name"],
            quantity=data["quantity"],
            payment_method=data["payment_method"],
            total=data["total"],
            date=parsed_date,
        )


class InvoiceManager:
    def __init__(self):
        self.invoices = []

    def get_next_invoice_id(self):
        if not self.invoices:
            return 1
        return max(invoice.id for invoice in self.invoices) + 1

    def get_invoice_by_id(self, invoice_id):
        for invoice in self.invoices:
            if invoice.id == invoice_id:
                return invoice
        return None

    def get_invoice_by_sale_id(self, sale_id):
        for invoice in self.invoices:
            if invoice.sale_id == sale_id:
                return invoice
        return None

    def create_invoice_from_sale(self, sale):
        existing_invoice = self.get_invoice_by_sale_id(sale.id)
        if existing_invoice:
            print(f"There is already an invoice for sale ID {sale.id}.")
            return None

        customer_name = sale.customer_name if sale.customer_name else "Walk-in"
        customer_id = sale.customer_id if sale.customer_id else None

        invoice = Invoice(
            id=self.get_next_invoice_id(),
            sale_id=sale.id,
            customer_id=customer_id,
            customer_name=customer_name,
            product_name=sale.product.name,
            quantity=sale.quantity,
            payment_method=sale.payment_method,
            total=sale.total,
        )

        self.invoices.append(invoice)
        print(f"Invoice #{invoice.id} generated successfully.")
        return invoice

    def list_invoices(self):
        if not self.invoices:
            print("No invoices generated.")
            return

        print("\n--- INVOICES ---")
        for invoice in self.invoices:
            print(
                f"Invoice ID: {invoice.id} | "
                f"Sale ID: {invoice.sale_id} | "
                f"Date: {invoice.date.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Customer: {invoice.customer_name} | "
                f"Product: {invoice.product_name} | "
                f"Qty: {invoice.quantity} | "
                f"Payment: {invoice.payment_method} | "
                f"Total: ${invoice.total:.2f}"
            )

    def print_invoice_detail(self, invoice_id):
        invoice = self.get_invoice_by_id(invoice_id)
        if not invoice:
            print("Invoice not found.")
            return

        print("\n--- INVOICE DETAIL ---")
        print(f"Invoice ID: {invoice.id}")
        print(f"Sale ID: {invoice.sale_id}")
        print(f"Date: {invoice.date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Customer: {invoice.customer_name}")
        print(f"Customer ID: {invoice.customer_id if invoice.customer_id else '-'}")
        print(f"Product: {invoice.product_name}")
        print(f"Quantity: {invoice.quantity}")
        print(f"Payment method: {invoice.payment_method}")
        print(f"Total: ${invoice.total:.2f}")

    def to_dict_list(self):
        return [invoice.to_dict() for invoice in self.invoices]

    def load_from_dict_list(self, invoices_data):
        self.invoices = []

        for item in invoices_data:
            invoice = Invoice.from_dict(item)
            self.invoices.append(invoice)