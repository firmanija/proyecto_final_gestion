class SalesAnalysis:
    def __init__(self):
        self.sales_data = []  

    def record_sale(self, product, quantity):
        """Registra una venta."""
        self.sales_data.append({'product': product, 'quantity': quantity})

    def most_sold_product(self):
        """Devuelve el producto más vendido."""
        sales_counts = {}
        for sale in self.sales_data:
            product = sale['product']
            quantity = sale['quantity']
            sales_counts[product] = sales_counts.get(product, 0) + quantity
        
        if sales_counts:
            return max(sales_counts.items(), key=lambda item: item[1])[0]  # Ajustado para evitar problemas
        return None

    def least_sold_product(self):
        """Devuelve el producto menos vendido."""
        sales_counts = {}
        for sale in self.sales_data:
            product = sale['product']
            quantity = sale['quantity']
            sales_counts[product] = sales_counts.get(product, 0) + quantity
        
        if sales_counts:
            return min(sales_counts.items(), key=lambda item: item[1])[0]  # Ajustado para evitar problemas
        return None

    def analyze_returns(self, returns_data):
        """Analiza las devoluciones y devuelve el producto más devuelto."""
        return_counts = {}
        for return_item in returns_data:  # Se asume que returns_data es una lista de productos devueltos
            product = return_item['product']
            return_counts[product] = return_counts.get(product, 0) + 1
        
        if return_counts:
            return max(return_counts.items(), key=lambda item: item[1])[0]  # Ajustado para evitar problemas
        return None
