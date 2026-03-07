from datetime import datetime


class Dashboard:
    def __init__(self, inventory, sales, petty_cash):
        self.inventory = inventory
        self.sales = sales
        self.petty_cash = petty_cash

    def get_total_revenue(self):
        return sum(sale.total for sale in self.sales.sales_data)

    def get_total_sales_count(self):
        return len(self.sales.sales_data)

    def get_today_sales_count(self):
        today = datetime.now().date()
        return sum(1 for sale in self.sales.sales_data if sale.date.date() == today)

    def get_today_revenue(self):
        today = datetime.now().date()
        return sum(sale.total for sale in self.sales.sales_data if sale.date.date() == today)

    def get_low_stock_products(self, threshold=5):
        low_stock = []

        for product in self.inventory.get_all_products().values():
            if product.stock <= threshold:
                low_stock.append(product)

        return low_stock

    def get_last_petty_cash_transaction(self):
        if not self.petty_cash.transactions:
            return None
        return self.petty_cash.transactions[-1]

    def show_dashboard(self):
        print("\n" + "=" * 55)
        print("                 BUSINESS DASHBOARD")
        print("=" * 55)

        print(f"Total sales count: {self.get_total_sales_count()}")
        print(f"Total revenue: ${self.get_total_revenue():.2f}")
        print(f"Today's sales count: {self.get_today_sales_count()}")
        print(f"Today's revenue: ${self.get_today_revenue():.2f}")
        print(f"Petty cash balance: ${self.petty_cash.balance:.2f}")

        last_transaction = self.get_last_petty_cash_transaction()
        if last_transaction:
            print(
                "Last petty cash movement: "
                f"{last_transaction.transaction_type.upper()} | "
                f"{last_transaction.description} | "
                f"${last_transaction.amount:.2f}"
            )
        else:
            print("Last petty cash movement: No transactions registered.")

        low_stock_products = self.get_low_stock_products()

        print("\n--- LOW STOCK PRODUCTS ---")
        if not low_stock_products:
            print("No low stock products.")
        else:
            for product in low_stock_products:
                print(
                    f"ID: {product.id} | "
                    f"Name: {product.name} | "
                    f"Stock: {product.stock}"
                )

        print("=" * 55)