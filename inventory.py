from product import Product
from transfer import Transfer

class Inventory:
    def __init__(self):
        self.products = {} 
        self.transfers = []

    def add_product(self, product):
        """Add a product to the inventory."""
        self.products[product.id] = product

    def get_product(self, product_id):
        """Return a product from the inventory by its id."""
        return self.products.get(product_id, None)

    def add_stock(self, product_id, quantity):
        """Increase the stock of a specific product."""
        product = self.get_product(product_id)
        if product:
            product.add_stock(quantity)
            print(f"Added {quantity} to {product.name}. New stock: {product.stock}")
        else:
            print("Product not found.")

    def remove_stock(self, product_id, quantity):
        """Decrease the stock of a specific product."""
        product = self.get_product(product_id)
        if product:
            product.remove_stock(quantity)
            print(f"Removed {quantity} from {product.name}. New stock: {product.stock}")
        else:
            print("Product not found.")

    def list_products(self):
        """List all products in the inventory."""
        for product in self.products.values():
            print(f"{product.id}: {product.name}, Stock: {product.stock}")
            

def transfer_product(self, product_id, quantity, from_location, to_location):
    """Perform a product transfer between locations."""
    product = self.get_product(product_id)
    if product:
        if quantity <= product.stock:
            transfer = Transfer(product_id, quantity, from_location, to_location)
            self.transfers.append(transfer)  
            product.remove_stock(quantity)  
            print(f"Transfer successful: {quantity} of Product ID {product_id} from {from_location} to {to_location}.")
        else:
            print("Not enough stock to transfer.")
    else:
        print("Product not found in inventory.")
   
   
def list_transfers(self):
        """Lis of all transferences made ."""
        for transfer in self.transfers:
            transfer.display_transfer_info()