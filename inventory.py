class Inventory:

    def __init__(self):
        self.products = {}
        self.transfers = []

    # ================================
    # PRODUCT MANAGEMENT
    # ================================

    def add_product(self, product):
        self.products[product.id] = product

    def get_product(self, product_id):
        return self.products.get(product_id)

    def get_all_products(self):
        return self.products

    def has_product(self, product_id):
        return product_id in self.products

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False

    def clear_products(self):
        self.products.clear()

    def list_products(self):
        print("\n--- PRODUCT LIST ---")

        for product in self.products.values():
            print(
                f"ID: {product.id} | "
                f"Name: {product.name} | "
                f"Price: ${product.price:.2f} | "
                f"Stock: {product.stock}"
            )

    # ================================
    # INVENTORY SUMMARY
    # ================================

    def inventory_summary(self):
        total_products = len(self.products)

        total_stock = sum(p.stock for p in self.products.values())

        total_value = sum(p.stock * p.price for p in self.products.values())

        print("\n--- INVENTORY SUMMARY ---")
        print(f"Products registered: {total_products}")
        print(f"Total units in stock: {total_stock}")
        print(f"Total inventory value: ${total_value:.2f}")

    # ================================
    # TRANSFERS
    # ================================

    def transfer_product(self, product_id, quantity, from_location, to_location):

        product = self.get_product(product_id)

        if not product:
            print("Product not found.")
            return

        if quantity > product.stock:
            print("Not enough stock for transfer.")
            return

        product.stock -= quantity

        transfer_record = {
            "product_id": product_id,
            "product_name": product.name,
            "quantity": quantity,
            "from": from_location,
            "to": to_location
        }

        self.transfers.append(transfer_record)

        print("Transfer recorded successfully.")

    def list_transfers(self):

        if not self.transfers:
            print("No transfers recorded.")
            return

        print("\n--- TRANSFERS ---")

        for t in self.transfers:
            print(
                f"Product: {t['product_name']} | "
                f"Qty: {t['quantity']} | "
                f"{t['from']} -> {t['to']}"
            )