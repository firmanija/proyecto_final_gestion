from inventory import Inventory
from petty_cash import Pettycash
from product import Product
from sale import Sales
from sales_analysis import SalesAnalysis
from data_managment import save_products_to_json, load_products_from_json

from cli_handlers import (
    show_main_menu,
    handle_inventory_menu,
    handle_sales_menu,
    handle_billing_menu,
    handle_petty_cash_menu,
    handle_reports_menu,
    handle_transfers_menu,
)


def seed(inventory: Inventory, petty_cash: Pettycash, sales: Sales, sales_analysis: SalesAnalysis) -> None:
    """
    Punto para cargar datos de prueba si más adelante querés usarlos.
    """
    pass


def main() -> None:
    inventory = Inventory()
    petty_cash = Pettycash()
    sales = Sales()
    sales_analysis = SalesAnalysis()

    # Cargar productos guardados
    products_data = load_products_from_json()
    for p in products_data:
        try:
            inventory.add_product(Product.from_dict(p))
        except Exception as e:
            print(f"Producto inválido en JSON: {e}")

    seed(inventory, petty_cash, sales, sales_analysis)

    while True:
        show_main_menu()
        choice = input("Seleccioná una opción: ").strip()

        if choice == "1":
            handle_inventory_menu(inventory)

        elif choice == "2":
            handle_sales_menu(inventory, sales, sales_analysis)

        elif choice == "3":
            handle_billing_menu()

        elif choice == "4":
            handle_petty_cash_menu(petty_cash)

        elif choice == "5":
            handle_reports_menu(inventory, sales_analysis)

        elif choice == "6":
            handle_transfers_menu(inventory)

        elif choice == "0":
            products_to_save = [
                prod.to_dict()
                for prod in inventory.get_all_products().values()
            ]
            save_products_to_json(products_to_save)
            print("\nDatos guardados correctamente.")
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intentá de nuevo.")


if __name__ == "__main__":
    main()