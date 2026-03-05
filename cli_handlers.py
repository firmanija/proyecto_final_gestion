from inventory import Inventory
from petty_cash import Pettycash
from product import Product


def show_menu() -> None:
    print("\n=== Sistema de Gestión ===")
    print("1) Agregar producto")
    print("2) Ver inventario")
    print("3) Caja chica")
    print("4) Eliminar producto")
    print("5) Borrar TODOS los productos")
    print("0) Salir")


def handle_add_product(inventory: Inventory) -> None:

    print("\n--- Agregar producto ---")
    mode = input("Modo: (1) Rápido  (2) Completo: ").strip()

    if mode == "2":
        print("Tip: Enter = saltear campo opcional.\n")

    # -------------------------
    # REQUERIDOS
    # -------------------------

    try:
        product_id = int(input("ID (requerido): ").strip())
    except ValueError:
        print("ID inválido.")
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
        cost_price = float(input("Precio de compra (requerido): ").strip())
        if cost_price < 0:
            print("El precio de compra no puede ser negativo.")
            return
    except ValueError:
        print("Precio de compra inválido.")
        return

    try:
        price = float(input("Precio de venta (requerido): ").strip())
        if price < 0:
            print("El precio de venta no puede ser negativo.")
            return
    except ValueError:
        print("Precio de venta inválido.")
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
            price=price,          # venta
            stock=stock,
            cost_price=cost_price # compra
        )

        inventory.add_product(product)
        print(f"\nProducto agregado (rápido): {product.name}")
        return

    # -------------------------
    # OPCIONALES (simple)
    # -------------------------

    brand_code = input("Brand code (Enter para saltar): ").strip() or None
    material = input("Material (Enter para saltar): ").strip() or None
    season = input("Season (Enter para saltar): ").strip() or None
    channel = input("Canal venta (Enter para saltar): ").strip() or None

    from datetime import datetime
    entry_date = datetime.now()

    product = Product(
        id=product_id,
        name=name,
        description=description,
        price=price,
        stock=stock,
        cost_price=cost_price,
        brand_code=brand_code,
        material=material,
        season=season,
        channel=channel,
        entry_date=entry_date
    )

    inventory.add_product(product)
    print(f"\nProducto agregado (completo): {product.name}")


def handle_view_inventory(inventory: Inventory) -> None:

    if not inventory.get_all_products():
        print("\nNo hay productos cargados.")
        return

    inventory.list_products()
    inventory.inventory_summary()


def handle_delete_product(inventory: Inventory) -> None:

    try:
        product_id = int(input("ID a eliminar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    if inventory.delete_product(product_id):
        print("Producto eliminado.")
    else:
        print("Producto no encontrado.")


def handle_clear_products(inventory: Inventory) -> None:

    confirm = input("¿Seguro que querés borrar TODOS los productos? (si/no): ").strip().lower()

    if confirm in ("si", "sí", "s", "yes", "y"):
        inventory.clear_products()
        print("Inventario borrado.")
    else:
        print("Operación cancelada.")


def handle_petty_cash(petty_cash: Pettycash) -> None:
    print("TODO: menu caja chica")