from product import Product
from transfer import Transfer


class Inventory:

    def __init__(self):
        self.products = {}
        self.transfers = []

    # -------------------------
    # METODOS AUXILIARES
    # -------------------------

    def get_all_products(self) -> dict:
        return self.products

    def has_product(self, product_id: int) -> bool:
        return product_id in self.products

    def delete_product(self, product_id: int) -> bool:
        return self.products.pop(product_id, None) is not None

    def clear_products(self) -> None:
        self.products.clear()

    # -------------------------
    # PRODUCTOS
    # -------------------------

    def add_product(self, product: Product) -> None:
        self.products[product.id] = product

    def get_product(self, product_id: int):
        return self.products.get(product_id, None)

    def add_stock(self, product_id: int, quantity: int) -> None:
        product = self.get_product(product_id)

        if product:
            product.add_stock(quantity)
            print(f"Added {quantity} to {product.name}. New stock: {product.stock}")
        else:
            print("Product not found.")

    def remove_stock(self, product_id: int, quantity: int) -> None:
        product = self.get_product(product_id)

        if product:
            product.remove_stock(quantity)
            print(f"Removed {quantity} from {product.name}. New stock: {product.stock}")
        else:
            print("Product not found.")

    # -------------------------
    # LISTADO INVENTARIO
    # -------------------------

    def list_products(self) -> None:

        print("\nArticulo | Cantidad | Compra | Venta | Margen | Margen % | Ganancia Total")
        print("-" * 95)

        for product in self.products.values():

            name = product.name
            stock = product.stock

            cost = product.cost_price
            sale = product.price

            cost_txt = f"{cost:.2f}" if isinstance(cost, (int, float)) else "N/A"
            sale_txt = f"{sale:.2f}" if isinstance(sale, (int, float)) else "N/A"

            if isinstance(cost, (int, float)) and isinstance(sale, (int, float)) and isinstance(stock, int):
                margin = sale - cost
                margin_percent = (margin / cost) * 100 if cost != 0 else 0.0
                total_profit = margin * stock

                margin_txt = f"{margin:.2f}"
                margin_percent_txt = f"{margin_percent:.1f}%"
                total_profit_txt = f"{total_profit:.2f}"
            else:
                margin_txt = "N/A"
                margin_percent_txt = "N/A"
                total_profit_txt = "N/A"

            print(
                f"{name} | {stock} | {cost_txt} | {sale_txt} | "
                f"{margin_txt} | {margin_percent_txt} | {total_profit_txt}"
            )

    def inventory_summary(self) -> None:
        total_cost = 0.0
        total_sale = 0.0

        for p in self.products.values():
            if (
                isinstance(p.cost_price, (int, float))
                and isinstance(p.price, (int, float))
                and isinstance(p.stock, int)
            ):
                total_cost += p.cost_price * p.stock
                total_sale += p.price * p.stock

        total_profit = total_sale - total_cost
        margin_pct = (total_profit / total_cost) * 100 if total_cost > 0 else 0.0

        print("\n--- Resumen inventario ---")
        print(f"Valor total compra (stock): {total_cost:.2f}")
        print(f"Valor total venta (stock):  {total_sale:.2f}")
        print(f"Ganancia potencial total:   {total_profit:.2f}")
        print(f"Margen potencial (%):       {margin_pct:.1f}%")

    # -------------------------
    # TRANSFERS
    # -------------------------

    def transfer_product(self, product_id, quantity, from_location, to_location):

        product = self.get_product(product_id)

        if product:

            if quantity <= product.stock:

                transfer = Transfer(product_id, quantity, from_location, to_location)
                self.transfers.append(transfer)

                product.remove_stock(quantity)

                print(
                    f"Transfer successful: {quantity} of Product ID {product_id} "
                    f"from {from_location} to {to_location}."
                )

            else:
                print("Not enough stock to transfer.")

        else:
            print("Product not found in inventory.")

    def list_transfers(self):

        for transfer in self.transfers:
            transfer.display_transfer_info()