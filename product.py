from datetime import datetime
from typing import Any, Dict, Optional, List


class Product:
    def __init__(
        self,
        id,
        name,
        description,
        price,
        stock,
        unique_code=None,
        brand_code=None,
        supplier_code=None,
        group_code=None,
        material=None,
        cost_price=None,
        includes_tax=False,
        entry_date=None,
        season=None,
        price_list_credit=None,
        price_list_cash=None,
        liquidation_price=None,
        is_liquidation=False,
        sizes=None,
        channel=None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.unique_code = unique_code
        self.brand_code = brand_code
        self.supplier_code = supplier_code
        self.group_code = group_code
        self.material = material
        self.cost_price = cost_price
        self.includes_tax = includes_tax
        self.entry_date = entry_date
        self.season = season
        self.price_list_credit = price_list_credit
        self.price_list_cash = price_list_cash
        self.liquidation_price = liquidation_price
        self.is_liquidation = is_liquidation
        self.sizes = sizes if sizes is not None else []
        self.channel = channel

    def to_dict(self) -> dict:
        """Convert the product into a dictionary to facilitate serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "unique_code": self.unique_code,
            "brand_code": self.brand_code,
            "supplier_code": self.supplier_code,
            "group_code": self.group_code,
            "material": self.material,
            "cost_price": self.cost_price,
            "includes_tax": self.includes_tax,
            "entry_date": self.entry_date.isoformat() if self.entry_date else None,
            "season": self.season,
            "price_list_credit": self.price_list_credit,
            "price_list_cash": self.price_list_cash,
            "liquidation_price": self.liquidation_price,
            "is_liquidation": self.is_liquidation,
            "sizes": self.sizes,
            "channel": self.channel,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """Rebuild a Product instance from a dict loaded from JSON."""
        entry_date_raw = data.get("entry_date")
        entry_date = None
        if entry_date_raw:
            try:
                entry_date = datetime.fromisoformat(entry_date_raw)
            except ValueError:
                entry_date = None

        sizes = data.get("sizes")
        if sizes is None:
            sizes = []
        elif not isinstance(sizes, list):
            sizes = [str(sizes)]

        return cls(
            id=int(data.get("id")),
            name=str(data.get("name", "")).strip(),
            description=str(data.get("description", "")).strip(),
            price=float(data.get("price", 0)),
            stock=int(data.get("stock", 0)),
            unique_code=data.get("unique_code"),
            brand_code=data.get("brand_code"),
            supplier_code=data.get("supplier_code"),
            group_code=data.get("group_code"),
            material=data.get("material"),
            cost_price=float(data["cost_price"]) if data.get("cost_price") not in (None, "") else None,
            includes_tax=bool(data.get("includes_tax", False)),
            entry_date=entry_date,
            season=data.get("season"),
            price_list_credit=float(data["price_list_credit"]) if data.get("price_list_credit") not in (None, "") else None,
            price_list_cash=float(data["price_list_cash"]) if data.get("price_list_cash") not in (None, "") else None,
            liquidation_price=float(data["liquidation_price"]) if data.get("liquidation_price") not in (None, "") else None,
            is_liquidation=bool(data.get("is_liquidation", False)),
            sizes=sizes,
            channel=data.get("channel"),
        )

    def display_info(self) -> None:
        """Show product information."""
        print(
            f"ID: {self.id}, Name: {self.name}, Description: {self.description}, "
            f"Price: {self.price}, Stock: {self.stock}, Channel: {self.channel}"
        )
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
            print(f"Sizes: {', '.join(map(str, self.sizes))}")

    def add_stock(self, quantity: int) -> None:
        """Add stock."""
        self.stock += quantity

    def remove_stock(self, quantity: int) -> None:
        """Eliminate stock."""
        if quantity <= self.stock:
            self.stock -= quantity
        else:
            print("Not enough stock.")

    def process_return(self, quantity: int) -> None:
        """Process a return updating stock."""
        self.add_stock(quantity)
        print(f"Processed return of {quantity} for {self.name}. New stock: {self.stock}")