from inventory import Inventory
from petty_cash import Pettycash
from product import Product
from data_managment import save_products_to_json, load_products_from_json

from cli_handlers import (
    show_menu,
    handle_add_product,
    handle_view_inventory,
    handle_petty_cash,
)


def seed(inventory: Inventory, petty_cash: Pettycash) -> None:
    pass


def main() -> None:
    inventory = Inventory()
    petty_cash = Pettycash()

    # Cargar productos guardados
    products_data = load_products_from_json()
    for p in products_data:
        try:
            inventory.add_product(Product.from_dict(p))
        except Exception as e:
            print(f"⚠️ Producto inválido en JSON, se omitió. Error: {e}")

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
            # Guardar productos al salir
            products_to_save = [
                prod.to_dict() for prod in inventory.get_all_products().values()
            ]
            save_products_to_json(products_to_save)
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()