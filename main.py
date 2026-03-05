from inventory import Inventory
from petty_cash import Pettycash
from product import Product
# from supplier import Supplier  # lo ajustamos después (hoy tu clase se llama Supllier)

def seed(inventory: Inventory, petty_cash: Pettycash) -> None:
    """
    Datos iniciales para probar el sistema.
    En este paso lo dejamos mínimo; luego lo completamos.
    """
    # Ejemplo mínimo:
    # inventory.add_product(Product(1, "Producto demo", 1000, 10))
    pass

def show_menu() -> None:
    print("\n=== Sistema de Gestión ===")
    print("1) Agregar producto")
    print("2) Ver inventario")
    print("3) Caja chica")
    print("0) Salir")

def handle_add_product(inventory: Inventory) -> None:
    print("\n--- Agregar producto ---")

    try:
        product_id = int(input("ID: ").strip())
    except ValueError:
        print("ID inválido. Debe ser un número.")
        return

    # Evitar IDs duplicados
    if product_id in inventory.products:
        print("Ya existe un producto con ese ID.")
        return

    name = input("Nombre: ").strip()
    if not name:
        print("El nombre no puede estar vacío.")
        return

    description = input("Descripción: ").strip()

    try:
        price = float(input("Precio: ").strip())
        if price < 0:
            print("El precio no puede ser negativo.")
            return
    except ValueError:
        print("Precio inválido.")
        return

    try:
        stock = int(input("Stock inicial: ").strip())
        if stock < 0:
            print("El stock no puede ser negativo.")
            return
    except ValueError:
        print("Stock inválido.")
        return

    product = Product(product_id, name, description, price, stock)
    inventory.add_product(product)

    print(f"Producto agregado: {product.name} (ID {product.id})")

def handle_view_inventory(inventory: Inventory) -> None:
    if not inventory.products:
        print("\nNo hay productos ingresados.")
        return

    inventory.list_products()
    # Fallback: intentar imprimir lo que haya adentro
    products = getattr(inventory, "products", None) or getattr(inventory, "_products", None)
    if not products:
        print("Inventario vacío.")
        return

    print("\n--- Inventario ---")
    for pid, product in products.items():
        name = getattr(product, "name", "N/A")
        price = getattr(product, "price", "N/A")
        stock = getattr(product, "stock", "N/A")
        print(f"ID: {pid} | {name} | Precio: {price} | Stock: {stock}")

def handle_petty_cash(petty_cash: Pettycash) -> None:
    print("TODO: menu caja chica")

def main() -> None:
    inventory = Inventory()
    petty_cash = Pettycash()
    seed(inventory, petty_cash)

    while True:
        show_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            handle_add_product(inventory)
        elif choice == "2":
            handle_view_inventory(inventory)
        elif choice == "3":
            handle_petty_cash(petty_cash)
        elif choice == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()

           
#credit_card = PaymentMethod("Tarjeta de Crédito")
#cash = PaymentMethod("Efectivo")
