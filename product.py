from datetime import datetime

class Product:
    def __init__(self, id, name, description, price, stock, unique_code=None, brand_code=None, 
                 supplier_code=None, group_code=None, material=None, cost_price=None, 
                 includes_tax=False, entry_date=None, season=None, price_list_credit=None,
                 price_list_cash=None, liquidation_price=None, is_liquidation=False, sizes=None):
        
        self.id=id
        self.name=name
        self.description=description
        self.price=price
        self.stock=stock
        self.unique_code=unique_code             # unique code for every item
        self.brand_code=brand_code               # unique code for every brand
        self.supplier_code=supplier_code         # unique code for every supplier
        self.group_code=group_code               # a group for different items (shirt, pants, etc)
        self.material=material                   # type of fabric for every item
        self.cost_price=cost_price               # item cost value 
        self.includes_tax=includes_tax           # add impositive taxes (iva)
        self.entry_date=entry_date               # date of entry  
        self.season=season                       # season for item (summer, winter, etc)
        self.price_list_credit=price_list_credit # price for credit card and non cash payments
        self.price_list_cash=price_list_cash     # price for cash payments
        self.liquidation_price=liquidation_price # price for items on sale 
        self.is_liquidation=is_liquidation       # put items on sale 
        self.sizes = sizes if sizes is not None else []

    def to_dict(self):
        "Convert the product into a dictionary to facilitate serialization."
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'unique_code': self.unique_code,
            'brand_code': self.brand_code,
            'supplier_code': self.supplier_code,
            'group_code': self.group_code,
            'material': self.material,
            'cost_price': self.cost_price,
            'includes_tax': self.includes_tax,
            'entry_date': self.entry_date.isoformat() if self.entry_date else None,
            'season': self.season,
            'price_list_credit': self.price_list_credit,
            'price_list_cash': self.price_list_cash,
            'liquidation_price': self.liquidation_price,
            'is_liquidation': self.is_liquidation,
            'sizes': self.sizes
              }
    
    
    def display_info(self):
        """Show product information."""
        print(f"ID: {self.id}, Name: {self.name}, Description: {self.description}, "
              f"Price: {self.price}, Stock: {self.stock}")
        if self.unique_code:
            print(f"Unique Code: {self.unique_code}")
        if self.brand_code:
            print(f"Brand Code: {self.brand_code}")
        if self.supplier_code:
            print(f"Supplier Code: {self.supplier_code}")
        if self.group_code:
            print(f"Group Code: {self.group_code}")
        if self.material:
            print(f"Material: {self.material}")
        if self.cost_price is not None:
            print(f"Cost Price: {self.cost_price}")
        print(f"Includes Taxes: {self.includes_tax}")
        print(f"Entry Date: {self.entry_date}, Season: {self.season}")
        if self.price_list_credit is not None:
            print(f"Price List (Credit): {self.price_list_credit}")
        if self.price_list_cash is not None:
            print(f"Price List (Cash): {self.price_list_cash}")
        if self.is_liquidation:
            print(f"Liquidation Price: {self.liquidation_price} (Item is on liquidation)")
        if self.sizes:
            print(f"Sizes: {', '.join(self.sizes)}")    
    
    def add_stock(self, quantity):
        """Add stock."""
        self.stock += quantity
    
    def remove_stock(self, quantity):
        """Eliminate stock."""
        if quantity <= self.stock:
            self.stock -= quantity        
        else:
            print("Not enough stock.")     