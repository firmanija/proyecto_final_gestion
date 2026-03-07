from datetime import datetime


class SalesAnalysis:

    def __init__(self):
        self.sales_counter = {}

    # =================================
    # REGISTRO DE VENTAS
    # =================================
    def record_sale(self, product_name, quantity):

        if product_name not in self.sales_counter:
            self.sales_counter[product_name] = 0

        self.sales_counter[product_name] += quantity

    # =================================
    # PRODUCTO MÁS VENDIDO
    # =================================
    def most_sold_product(self):

        if not self.sales_counter:
            return None

        return max(self.sales_counter, key=self.sales_counter.get)

    # =================================
    # PRODUCTO MENOS VENDIDO
    # =================================
    def least_sold_product(self):

        if not self.sales_counter:
            return None

        return min(self.sales_counter, key=self.sales_counter.get)

    # =================================
    # INGRESOS DEL DÍA
    # =================================
    def daily_revenue(self, sales):

        today = datetime.now().date()

        total = 0

        for sale in sales.sales_data:

            if sale.date.date() == today:
                total += sale.total

        return total

    # =================================
    # REPORTE FINANCIERO DEL DÍA
    # =================================
    def daily_report(self, sales):

        today = datetime.now().date()

        total_sales = 0
        total_revenue = 0

        for sale in sales.sales_data:

            if sale.date.date() == today:
                total_sales += 1
                total_revenue += sale.total

        print("\n--- DAILY FINANCIAL REPORT ---")
        print(f"Date: {today}")
        print(f"Sales today: {total_sales}")
        print(f"Revenue today: ${total_revenue:.2f}")