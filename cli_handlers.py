from datetime import datetime

from inventory import Inventory
from petty_cash import Pettycash
from product import Product
from sale import Sales
from sales_analysis import SalesAnalysis


# =========================================================
# MENU PRINCIPAL
# =========================================================
def show_main_menu() -> None:
    print("\n" + "=" * 55)
    print("         SISTEMA DE GESTIÓN PARA COMERCIOS")
    print("=" * 55)
    print("1) Inventario")
    print("2) Ventas")
    print("3) Facturación")
    print("4) Caja chica")
    print("5) Reportes")
    print("6) Transferencias")
    print("0) Salir")


# =========================================================
# INVENTARIO
# =========================================================
def show_inventory_menu() -> None:
    print("\n--- INVENTARIO ---")
    print("1) Agregar producto")
    print("2) Ver inventario")
    print("3) Eliminar producto")
    print("4) Borrar todos los productos")
    print("0) Volver")


def handle_inventory_menu(inventory: Inventory) -> None:
    while True:
        show_inventory_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            handle_add_product(inventory)
        elif choice == "2":
            handle_view_inventory(inventory)
        elif choice == "3":
            handle_delete_product(inventory)
        elif choice == "4":
            handle_clear_products(inventory)
        elif choice == "0":
            break
        else:
            print("Opción inválida.")


def handle_add_product(inventory: Inventory) -> None:
    print("\n--- Agregar producto ---")
    mode = input("Modo: (1) Rápido (2) Completo: ").strip()

    if mode == "2":
        print("Tip: Enter = saltear campo opcional.\n")

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

    if mode != "2":
        product = Product(
            id=product_id,
            name=name,
            description=description,
            price=price,
            stock=stock,
            cost_price=cost_price
        )
        inventory.add_product(product)
        print(f"\nProducto agregado: {product.name}")
        return

    brand_code = input("Brand code (Enter para saltar): ").strip() or None
    material = input("Material (Enter para saltar): ").strip() or None
    season = input("Season (Enter para saltar): ").strip() or None
    channel = input("Canal venta (Enter para saltar): ").strip() or None

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
        product_id = int(input("ID del producto a eliminar: ").strip())
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


# =========================================================
# VENTAS
# =========================================================
def show_sales_menu() -> None:
    print("\n--- VENTAS ---")
    print("1) Registrar venta")
    print("2) Ver módulo ventas")
    print("0) Volver")


def handle_sales_menu(inventory: Inventory, sales: Sales, sales_analysis: SalesAnalysis) -> None:
    while True:
        show_sales_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            handle_register_sale(inventory, sales, sales_analysis)
        elif choice == "2":
            print("Módulo ventas preparado para expansión web.")
            print("Acá después podés listar ventas, filtrar por fecha, cliente o medio de pago.")
        elif choice == "0":
            break
        else:
            print("Opción inválida.")


def handle_register_sale(
    inventory: Inventory,
    sales: Sales,
    sales_analysis: SalesAnalysis
) -> None:
    if not inventory.get_all_products():
        print("No hay productos cargados para vender.")
        return

    try:
        product_id = int(input("ID del producto vendido: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    product = inventory.get_product(product_id)
    if not product:
        print("Producto no encontrado.")
        return

    try:
        quantity = int(input("Cantidad: ").strip())
        if quantity <= 0:
            print("La cantidad debe ser mayor a 0.")
            return
    except ValueError:
        print("Cantidad inválida.")
        return

    if quantity > product.stock:
        print("No hay stock suficiente.")
        return

    payment_method = input("Medio de pago: ").strip() or "Efectivo"
    employee = input("Empleado que realizó la venta: ").strip() or "Sistema"

    sale_id = len(sales.sales_data) + 1

    sales.record_sale(
        id=sale_id,
        product=product,
        employee=employee,
        quantity=quantity,
        payment_method=payment_method
    )

    product.remove_stock(quantity)
    sales_analysis.record_sale(product.name, quantity)

    total = product.price * quantity
    print(f"Venta registrada correctamente. Total: ${total:.2f}")


# =========================================================
# FACTURACION
# =========================================================
def show_billing_menu() -> None:
    print("\n--- FACTURACIÓN ---")
    print("1) Emitir comprobante")
    print("2) Ver estado del módulo")
    print("0) Volver")


def handle_billing_menu() -> None:
    while True:
        show_billing_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            print("Factura generada (simulación).")
            print("Más adelante acá podés conectar ticket, factura A/B/C o exportación PDF.")
        elif choice == "2":
            print("Módulo de facturación listo como parte del esqueleto principal.")
        elif choice == "0":
            break
        else:
            print("Opción inválida.")


# =========================================================
# CAJA CHICA
# =========================================================
def show_petty_cash_menu() -> None:
    print("\n--- CAJA CHICA ---")
    print("1) Abrir caja")
    print("2) Registrar gasto")
    print("3) Ver movimientos")
    print("4) Cierre de caja")
    print("0) Volver")


def handle_petty_cash_menu(petty_cash: Pettycash) -> None:
    while True:
        show_petty_cash_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            try:
                employee_id = input("Empleado responsable: ").strip() or "Sistema"
                initial_amount = float(input("Monto inicial: ").strip())
                petty_cash.open_cash_register(employee_id, initial_amount)
            except ValueError:
                print("Monto inválido.")

        elif choice == "2":
            try:
                employee_id = input("Empleado responsable: ").strip() or "Sistema"
                amount = float(input("Monto del gasto: ").strip())
                description = input("Descripción: ").strip() or "Gasto sin detalle"
                petty_cash.add_expense(employee_id, amount, description)
            except ValueError:
                print("Monto inválido.")

        elif choice == "3":
            if not petty_cash.transactions:
                print("No hay movimientos registrados.")
            else:
                print("\nMovimientos de caja:")
                for i, trans in enumerate(petty_cash.transactions, start=1):
                    print(
                        f"{i}) {trans.date.strftime('%Y-%m-%d %H:%M:%S')} | "
                        f"{trans.description} | ${trans.amount:.2f} | "
                        f"Empleado: {trans.employee_id}"
                    )
                print(f"Saldo actual: ${petty_cash.balance:.2f}")

        elif choice == "4":
            petty_cash.print_closing_report()

        elif choice == "0":
            break

        else:
            print("Opción inválida.")


# =========================================================
# REPORTES
# =========================================================
def show_reports_menu() -> None:
    print("\n--- REPORTES ---")
    print("1) Resumen de inventario")
    print("2) Producto más vendido")
    print("3) Producto menos vendido")
    print("0) Volver")


def handle_reports_menu(inventory: Inventory, sales_analysis: SalesAnalysis) -> None:
    while True:
        show_reports_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            if not inventory.get_all_products():
                print("No hay productos cargados.")
            else:
                inventory.inventory_summary()

        elif choice == "2":
            product = sales_analysis.most_sold_product()
            if product:
                print(f"Producto más vendido: {product}")
            else:
                print("Todavía no hay ventas registradas.")

        elif choice == "3":
            product = sales_analysis.least_sold_product()
            if product:
                print(f"Producto menos vendido: {product}")
            else:
                print("Todavía no hay ventas registradas.")

        elif choice == "0":
            break

        else:
            print("Opción inválida.")


# =========================================================
# TRANSFERENCIAS
# =========================================================
def show_transfers_menu() -> None:
    print("\n--- TRANSFERENCIAS ---")
    print("1) Registrar transferencia")
    print("2) Ver transferencias")
    print("0) Volver")


def handle_transfers_menu(inventory: Inventory) -> None:
    while True:
        show_transfers_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            try:
                product_id = int(input("ID del producto: ").strip())
                quantity = int(input("Cantidad a transferir: ").strip())
                from_location = input("Desde ubicación: ").strip()
                to_location = input("Hacia ubicación: ").strip()

                inventory.transfer_product(product_id, quantity, from_location, to_location)
            except ValueError:
                print("Datos inválidos.")

        elif choice == "2":
            if not inventory.transfers:
                print("No hay transferencias registradas.")
            else:
                inventory.list_transfers()

        elif choice == "0":
            break

        else:
            print("Opción inválida.")