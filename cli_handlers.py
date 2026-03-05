from inventory import Inventory
from petty_cash import Pettycash
from product import Product


def show_menu() -> None:
    print("\n=== Sistema de Gestión ===")
    print("1) Agregar producto")
    print("2) Ver inventario")
    print("3) Caja chica")
    print("0) Salir")


def handle_add_product(inventory: Inventory) -> None:
    print("\n--- Agregar producto ---")
    mode = input("Modo: (1) Rápido  (2) Completo: ").strip()

    if mode == "2":
        print("Tip: Enter = saltear campo opcional. Escribí FIN para terminar carga opcional.\n")

    def ask_str(label: str, optional: bool = True):
        val = input(f"{label}: ").strip()
        if val.upper() == "FIN":
            return "FIN"
        if not val and optional:
            return None
        return val

    def ask_float(label: str, optional: bool = True):
        while True:
            val = input(f"{label}: ").strip()
            if val.upper() == "FIN":
                return "FIN"
            if not val and optional:
                return None
            try:
                return float(val)
            except ValueError:
                print("Valor inválido. Debe ser un número.")

    def ask_bool(label: str, default: bool = False):
        val = input(f"{label} (s/n) [default {'s' if default else 'n'}]: ").strip().lower()
        if val in ("s", "si", "sí", "y", "yes"):
            return True
        if val in ("n", "no"):
            return False
        return default

    # -------------------------
    # REQUERIDOS
    # -------------------------

    try:
        product_id = int(input("ID (requerido): ").strip())
    except ValueError:
        print("ID inválido. Debe ser un número.")
        return

    if inventory.has_product(product_id):
        print("Ya existe un producto con ese ID.")
        return

    name = input("Nombre (requerido): ").strip()
    if not name:
        print("El nombre no puede estar vacío.")
        return

    description = input("Descripción (requerido): ").strip()
    if not description:
        print("La descripción no puede estar vacía.")
        return

    try:
        price = float(input("Precio (requerido): ").strip())
        if price < 0:
            print("El precio no puede ser negativo.")
            return
    except ValueError:
        print("Precio inválido.")
        return

    try:
        stock = int(input("Stock inicial (requerido): ").strip())
        if stock < 0:
            print("El stock no puede ser negativo.")
            return
    except ValueError:
        print("Stock inválido.")
        return

    # -------------------------
    # MODO RAPIDO
    # -------------------------

    if mode != "2":
        product = Product(
            id=product_id,
            name=name,
            description=description,
            price=price,
            stock=stock,
        )
        inventory.add_product(product)
        print(f"\nProducto agregado (rápido): {product.name} (ID {product.id})")
        return

    # -------------------------
    # OPCIONALES
    # -------------------------

    unique_code = ask_str("Unique code")
    if unique_code == "FIN":
        unique_code = None

    brand_code = ask_str("Brand code")
    if brand_code == "FIN":
        brand_code = None

    supplier_code = ask_str("Supplier code")
    if supplier_code == "FIN":
        supplier_code = None

    group_code = ask_str("Group code (ej: remeras, buzos)")
    if group_code == "FIN":
        group_code = None

    material = ask_str("Material")
    if material == "FIN":
        material = None

    cost_price = ask_float("Cost price")
    if cost_price == "FIN":
        cost_price = None

    includes_tax = ask_bool("¿Incluye impuestos?", default=False)

    season = ask_str("Season (ej: summer, winter)")
    if season == "FIN":
        season = None

    price_list_credit = ask_float("Precio lista crédito")
    if price_list_credit == "FIN":
        price_list_credit = None

    price_list_cash = ask_float("Precio lista efectivo")
    if price_list_cash == "FIN":
        price_list_cash = None

    is_liquidation = ask_bool("¿Está en liquidación?", default=False)
    liquidation_price = None
    if is_liquidation:
        liquidation_price = ask_float("Precio liquidación", optional=False)
        if liquidation_price == "FIN":
            liquidation_price = None

    sizes_raw = ask_str("Talles (separados por coma, ej: S,M,L)")
    if sizes_raw == "FIN" or sizes_raw is None:
        sizes = []
    else:
        sizes = [s.strip() for s in sizes_raw.split(",") if s.strip()]

    channel = ask_str("Canal (retail / ecommerce / wholesale)")
    if channel == "FIN":
        channel = None

    from datetime import datetime
    entry_date = datetime.now()

    product = Product(
        id=product_id,
        name=name,
        description=description,
        price=price,
        stock=stock,
        unique_code=unique_code,
        brand_code=brand_code,
        supplier_code=supplier_code,
        group_code=group_code,
        material=material,
        cost_price=cost_price,
        includes_tax=includes_tax,
        entry_date=entry_date,
        season=season,
        price_list_credit=price_list_credit,
        price_list_cash=price_list_cash,
        liquidation_price=liquidation_price,
        is_liquidation=is_liquidation,
        sizes=sizes,
        channel=channel,
    )

    inventory.add_product(product)
    print(f"\nProducto agregado (completo): {product.name} (ID {product.id})")


def handle_view_inventory(inventory: Inventory) -> None:
    if not inventory.get_all_products():
        print("\nNo hay productos ingresados.")
        return

    inventory.list_products()


def handle_petty_cash(petty_cash: Pettycash) -> None:
    print("TODO: menu caja chica")