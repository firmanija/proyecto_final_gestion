import json
import os


PRODUCTS_FILE = "products.json"
SALES_FILE = "sales.json"
CUSTOMERS_FILE = "customers.json"


# =========================================================
# PRODUCTS
# =========================================================

def save_products_to_json(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=4)


def load_products_from_json():
    if not os.path.exists(PRODUCTS_FILE):
        return []

    with open(PRODUCTS_FILE, "r") as f:
        return json.load(f)


# =========================================================
# SALES
# =========================================================

def save_sales_to_json(sales):
    with open(SALES_FILE, "w") as f:
        json.dump(sales, f, indent=4)


def load_sales_from_json():
    if not os.path.exists(SALES_FILE):
        return []

    with open(SALES_FILE, "r") as f:
        return json.load(f)


# =========================================================
# CUSTOMERS
# =========================================================

def save_customers_to_json(customers):
    with open(CUSTOMERS_FILE, "w") as f:
        json.dump(customers, f, indent=4)


def load_customers_from_json():
    if not os.path.exists(CUSTOMERS_FILE):
        return []

    with open(CUSTOMERS_FILE, "r") as f:
        return json.load(f)