import json
from product import Product  # Asegúrate de importar la clase Product

def save_products_to_json(products, filename='products.json'):
    """Saves the list of products to a JSON file."""
    with open(filename, 'w') as file:
        json.dump([product.to_dict() for product in products], file, indent=4)

def load_products_from_json(filename='products.json'):
    """Uploads products list to a JSON file."""
    try:
        with open(filename, 'r') as file:
            products_data = json.load(file)
            return [Product(**data) for data in products_data]
    except FileNotFoundError:
        print(f"{filename} Not found. Returning to empty products.")
        return []