from datetime import datetime

from inventory import Inventory
from petty_cash import Pettycash
from product import Product
from sale import Sales
from sales_analysis import SalesAnalysis
from customer import Customer, CustomerManager
from invoice import InvoiceManager


# =========================================================
# MENU PRINCIPAL
# =========================================================
def show_main_menu() -> None:
    print("\n" + "=" * 55)
    print("         SISTEMA DE GESTIÓN PARA COMERCIOS")
    print("=" * 55)
    print("1) Dashboard")
    print("2) Inventario")
    print("3) Ventas")
    print("4) Facturación")
    print("5) Caja chica")
    print("6) Reportes")
    print("7) Transferencias")
    print("8) Clientes")
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

    try:
        product_id = int(input("ID: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    if inventory.has_product(product_id):
        print("Ya existe un producto con ese ID.")
        return

    name = input("Nombre: ").strip()
    description = input("Descripción: ").strip()

    try:
        cost_price = float(input("Precio de compra: ").strip())
        price = float(input("Precio de venta: ").strip())
        stock = int(input("Stock inicial: ").strip())
    except ValueError:
        print("Valores numéricos inválidos.")
        return

    product = Product(
        id=product_id,
        name=name,
        description=description,
        price=price,
        stock=stock,
        cost_price=cost_price
    )

    inventory.add_product(product)

    print("Producto agregado correctamente.")


def handle_view_inventory(inventory: Inventory) -> None:
    if not inventory.get_all_products():
        print("No hay productos cargados.")
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
    confirm = input("¿Seguro que querés borrar todo el inventario? (si/no): ").lower()

    if confirm in ("si", "s", "yes", "y"):
        inventory.clear_products()
        print("Inventario eliminado.")
    else:
        print("Operación cancelada.")


# =========================================================
# VENTAS
# =========================================================
def show_sales_menu() -> None:
    print("\n--- VENTAS ---")
    print("1) Registrar venta")
    print("2) Ver historial de ventas")
    print("3) Ver resumen de ventas")
    print("0) Volver")


def handle_sales_menu(
    inventory: Inventory,
    sales: Sales,
    sales_analysis: SalesAnalysis,
    petty_cash: Pettycash,
    customers: CustomerManager,
    current_user
) -> None:

    while True:
        show_sales_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            handle_register_sale(
                inventory,
                sales,
                sales_analysis,
                petty_cash,
                customers,
                current_user
            )

        elif choice == "2":
            sales.list_sales()

        elif choice == "3":
            print("\n--- RESUMEN DE VENTAS ---")
            print(f"Cantidad total de ventas: {sales.get_sales_count()}")
            print(f"Recaudación total: ${sales.get_total_revenue():.2f}")

        elif choice == "0":
            break

        else:
            print("Opción inválida.")


def handle_register_sale(
    inventory: Inventory,
    sales: Sales,
    sales_analysis: SalesAnalysis,
    petty_cash: Pettycash = None,
    customers: CustomerManager = None,
    current_user=None
) -> None:

    if not inventory.get_all_products():
        print("No hay productos cargados.")
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
    except ValueError:
        print("Cantidad inválida.")
        return

    if quantity <= 0:
        print("La cantidad debe ser mayor a 0.")
        return

    if quantity > product.stock:
        print("Stock insuficiente.")
        return

    payment_method = input("Medio de pago: ").strip()

    employee = "Sistema"
    if current_user:
        employee = current_user.username

    customer_id = None
    customer_name = None

    if customers:
        use_customer = input("¿Asociar cliente? (si/no): ").lower()

        if use_customer in ("si", "s", "yes", "y"):
            customers.list_customers()

            try:
                selected_customer_id = int(input("ID cliente: ").strip())
                customer = customers.get_customer(selected_customer_id)

                if customer:
                    customer_id = customer.id
                    customer_name = customer.name
                else:
                    print("Cliente no encontrado. La venta seguirá como Walk-in.")

            except ValueError:
                print("ID inválido. La venta seguirá como Walk-in.")

    sale_id = sales.get_next_sale_id()

    sale = sales.record_sale(
        id=sale_id,
        product=product,
        employee=employee,
        quantity=quantity,
        payment_method=payment_method,
        customer_id=customer_id,
        customer_name=customer_name
    )

    product.remove_stock(quantity)

    sales_analysis.record_sale(product.name, quantity)

    total = sale.total

    if petty_cash and payment_method.lower() in ["cash", "efectivo"]:
        petty_cash.add_income(employee, total, "Cash sale")

    print(f"Venta registrada correctamente por {employee}. Total: ${total:.2f}")

    if product.stock <= 5:
        print(
            f"⚠ ALERTA DE STOCK BAJO: {product.name} quedó con {product.stock} unidades."
        )


# =========================================================
# FACTURACION
# =========================================================
def show_billing_menu() -> None:
    print("\n--- FACTURACIÓN ---")
    print("1) Generar factura desde venta")
    print("2) Ver historial de facturas")
    print("3) Ver detalle de factura")
    print("4) Exportar factura a TXT")
    print("5) Exportar factura a PDF")
    print("0) Volver")


def handle_billing_menu(sales: Sales, invoices: InvoiceManager) -> None:
    while True:
        show_billing_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            if not sales.sales_data:
                print("No hay ventas registradas.")
                continue

            sales.list_sales()

            try:
                sale_id = int(input("ID venta: "))
            except ValueError:
                print("ID inválido.")
                continue

            selected_sale = None

            for sale in sales.sales_data:
                if sale.id == sale_id:
                    selected_sale = sale

            if not selected_sale:
                print("Venta no encontrada.")
                continue

            invoices.create_invoice_from_sale(selected_sale)

        elif choice == "2":
            invoices.list_invoices()

        elif choice == "3":
            try:
                invoice_id = int(input("ID factura: "))
                invoices.print_invoice_detail(invoice_id)
            except ValueError:
                print("ID inválido.")

        elif choice == "4":
            try:
                invoice_id = int(input("ID factura: "))
                invoices.export_invoice_to_txt(invoice_id)
            except ValueError:
                print("ID inválido.")

        elif choice == "5":
            try:
                invoice_id = int(input("ID factura: "))
                invoices.export_invoice_to_pdf(invoice_id)
            except ValueError:
                print("ID inválido.")

        elif choice == "0":
            break

        else:
            print("Opción inválida.")


# =========================================================
# CAJA CHICA
# =========================================================
def show_petty_cash_menu():
    print("\n--- CAJA CHICA ---")
    print("1) Abrir caja")
    print("2) Registrar ingreso")
    print("3) Registrar gasto")
    print("4) Ver movimientos")
    print("0) Volver")


def handle_petty_cash_menu(petty_cash: Pettycash):
    while True:
        show_petty_cash_menu()
        choice = input("Opción: ")

        if choice == "1":
            employee = input("Empleado: ")
            amount = float(input("Monto inicial: "))
            petty_cash.open_cash_register(employee, amount)

        elif choice == "2":
            employee = input("Empleado: ")
            amount = float(input("Monto: "))
            desc = input("Descripción: ")
            petty_cash.add_income(employee, amount, desc)

        elif choice == "3":
            employee = input("Empleado: ")
            amount = float(input("Monto: "))
            desc = input("Descripción: ")
            petty_cash.add_expense(employee, amount, desc)

        elif choice == "4":
            petty_cash.list_transactions()

        elif choice == "0":
            break

        else:
            print("Opción inválida.")


# =========================================================
# REPORTES
# =========================================================
def show_reports_menu():
    print("\n--- REPORTES ---")
    print("1) Resumen inventario")
    print("2) Producto más vendido")
    print("3) Producto menos vendido")
    print("4) Reporte financiero del día")
    print("0) Volver")


def handle_reports_menu(inventory, sales_analysis, sales):
    while True:
        show_reports_menu()
        choice = input("Opción: ")

        if choice == "1":
            inventory.inventory_summary()

        elif choice == "2":
            print("Más vendido:", sales_analysis.most_sold_product())

        elif choice == "3":
            print("Menos vendido:", sales_analysis.least_sold_product())

        elif choice == "4":
            sales_analysis.daily_report(sales)

        elif choice == "0":
            break

        else:
            print("Opción inválida.")


# =========================================================
# TRANSFERENCIAS
# =========================================================
def show_transfers_menu():
    print("\n--- TRANSFERENCIAS ---")
    print("1) Registrar transferencia")
    print("2) Ver transferencias")
    print("0) Volver")


def handle_transfers_menu(inventory: Inventory):
    while True:
        show_transfers_menu()
        choice = input("Opción: ")

        if choice == "1":
            try:
                product_id = int(input("ID producto: "))
                quantity = int(input("Cantidad: "))
            except ValueError:
                print("Valores inválidos.")
                continue

            origin = input("Desde: ")
            destination = input("Hacia: ")

            inventory.transfer_product(product_id, quantity, origin, destination)

        elif choice == "2":
            inventory.list_transfers()

        elif choice == "0":
            break

        else:
            print("Opción inválida.")


# =========================================================
# CLIENTES
# =========================================================
def show_customers_menu():
    print("\n--- CLIENTES ---")
    print("1) Agregar cliente")
    print("2) Ver clientes")
    print("3) Buscar cliente")
    print("4) Eliminar cliente")
    print("0) Volver")


def handle_customers_menu(customers: CustomerManager):
    while True:
        show_customers_menu()
        choice = input("Opción: ")

        if choice == "1":
            try:
                cid = int(input("ID cliente: "))
            except ValueError:
                print("ID inválido.")
                continue

            name = input("Nombre: ")
            email = input("Email: ")
            phone = input("Teléfono: ")
            address = input("Dirección: ")
            tax_id = input("CUIT: ")

            customer = Customer(cid, name, email, phone, address, tax_id)
            customers.add_customer(customer)

        elif choice == "2":
            customers.list_customers()

        elif choice == "3":
            name = input("Nombre a buscar: ")
            results = customers.search_by_name(name)

            for c in results:
                print(c.id, c.name)

        elif choice == "4":
            try:
                cid = int(input("ID cliente: "))
                customers.delete_customer(cid)
            except ValueError:
                print("ID inválido.")

        elif choice == "0":
            break

        else:
            print("Opción inválida.")