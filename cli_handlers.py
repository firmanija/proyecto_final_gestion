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
    print("1) Inventario")
    print("2) Ventas")
    print("3) Facturación")
    print("4) Caja chica")
    print("5) Reportes")
    print("6) Transferencias")
    print("7) Clientes")
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
    confirm = input(
        "¿Seguro que querés borrar TODOS los productos? (si/no): "
    ).strip().lower()

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
    print("2) Ver historial de ventas")
    print("3) Ver resumen de ventas")
    print("0) Volver")


def handle_sales_menu(
    inventory: Inventory,
    sales: Sales,
    sales_analysis: SalesAnalysis,
    petty_cash: Pettycash,
    customers: CustomerManager
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
                customers
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
    customers: CustomerManager = None
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

    payment_method = input("Medio de pago (cash/qr/card/transfer): ").strip().lower()
    employee = input("Empleado que realizó la venta: ").strip() or "Sistema"

    customer_id = None
    customer_name = None

    if customers:
        use_customer = input("¿Asociar cliente a la venta? (si/no): ").strip().lower()

        if use_customer in ("si", "sí", "s", "yes", "y"):
            if not customers.get_all_customers():
                print("No hay clientes registrados. La venta seguirá como Walk-in.")
            else:
                customers.list_customers()
                try:
                    selected_customer_id = int(input("ID del cliente: ").strip())
                    customer = customers.get_customer(selected_customer_id)

                    if customer:
                        customer_id = customer.id
                        customer_name = customer.name
                    else:
                        print("Cliente no encontrado. La venta seguirá como Walk-in.")
                except ValueError:
                    print("ID de cliente inválido. La venta seguirá como Walk-in.")

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

    if petty_cash and payment_method in ["cash", "efectivo"]:
        petty_cash.add_income(employee, total, "Cash sale")

    print(f"Venta registrada correctamente. Total: ${total:.2f}")


# =========================================================
# FACTURACION
# =========================================================
def show_billing_menu() -> None:
    print("\n--- FACTURACIÓN ---")
    print("1) Generar factura desde venta")
    print("2) Ver historial de facturas")
    print("3) Ver detalle de factura")
    print("0) Volver")


def handle_billing_menu(sales: Sales, invoices: InvoiceManager) -> None:
    while True:
        show_billing_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            handle_generate_invoice_from_sale(sales, invoices)

        elif choice == "2":
            invoices.list_invoices()

        elif choice == "3":
            handle_invoice_detail(invoices)

        elif choice == "0":
            break

        else:
            print("Opción inválida.")


def handle_generate_invoice_from_sale(sales: Sales, invoices: InvoiceManager) -> None:
    if not sales.sales_data:
        print("No hay ventas registradas para facturar.")
        return

    sales.list_sales()

    try:
        sale_id = int(input("ID de la venta a facturar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    selected_sale = None
    for sale in sales.sales_data:
        if sale.id == sale_id:
            selected_sale = sale
            break

    if not selected_sale:
        print("Venta no encontrada.")
        return

    invoices.create_invoice_from_sale(selected_sale)


def handle_invoice_detail(invoices: InvoiceManager) -> None:
    if not invoices.invoices:
        print("No hay facturas generadas.")
        return

    try:
        invoice_id = int(input("ID de factura: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    invoices.print_invoice_detail(invoice_id)


# =========================================================
# CAJA CHICA
# =========================================================
def show_petty_cash_menu() -> None:
    print("\n--- CAJA CHICA ---")
    print("1) Abrir caja")
    print("2) Registrar ingreso")
    print("3) Registrar gasto")
    print("4) Ver movimientos")
    print("5) Modificar movimiento")
    print("6) Eliminar movimiento")
    print("7) Cierre de caja")
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
                amount = float(input("Monto del ingreso: ").strip())
                description = input("Descripción: ").strip() or "Ingreso sin detalle"
                petty_cash.add_income(employee_id, amount, description)
            except ValueError:
                print("Monto inválido.")

        elif choice == "3":
            try:
                employee_id = input("Empleado responsable: ").strip() or "Sistema"
                amount = float(input("Monto del gasto: ").strip())
                description = input("Descripción: ").strip() or "Gasto sin detalle"
                petty_cash.add_expense(employee_id, amount, description)
            except ValueError:
                print("Monto inválido.")

        elif choice == "4":
            petty_cash.list_transactions()
            print(f"Saldo actual: ${petty_cash.balance:.2f}")

        elif choice == "5":
            if not petty_cash.transactions:
                print("No hay movimientos para modificar.")
                continue

            petty_cash.list_transactions()

            try:
                index = int(input("Número de movimiento a modificar: ").strip()) - 1
                new_amount = float(input("Nuevo monto: ").strip())
                new_description = input("Nueva descripción: ").strip() or "Movimiento editado"
                petty_cash.modify_transaction(index, new_amount, new_description)
            except ValueError:
                print("Datos inválidos.")

        elif choice == "6":
            if not petty_cash.transactions:
                print("No hay movimientos para eliminar.")
                continue

            petty_cash.list_transactions()

            try:
                index = int(input("Número de movimiento a eliminar: ").strip()) - 1
                petty_cash.delete_transaction(index)
            except ValueError:
                print("Índice inválido.")

        elif choice == "7":
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

                inventory.transfer_product(
                    product_id,
                    quantity,
                    from_location,
                    to_location
                )
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


# =========================================================
# CLIENTES
# =========================================================
def show_customers_menu() -> None:
    print("\n--- CLIENTES ---")
    print("1) Agregar cliente")
    print("2) Ver clientes")
    print("3) Buscar cliente por nombre")
    print("4) Eliminar cliente")
    print("0) Volver")


def handle_customers_menu(customers: CustomerManager) -> None:
    while True:
        show_customers_menu()
        choice = input("Opción: ").strip()

        if choice == "1":
            handle_add_customer(customers)
        elif choice == "2":
            customers.list_customers()
        elif choice == "3":
            handle_search_customer(customers)
        elif choice == "4":
            handle_delete_customer(customers)
        elif choice == "0":
            break
        else:
            print("Opción inválida.")


def handle_add_customer(customers: CustomerManager) -> None:
    print("\n--- Agregar cliente ---")

    try:
        customer_id_input = input("ID cliente (Enter para automático): ").strip()
        if customer_id_input:
            customer_id = int(customer_id_input)
        else:
            customer_id = customers.get_next_customer_id()
    except ValueError:
        print("ID inválido.")
        return

    if customers.has_customer(customer_id):
        print("Ya existe un cliente con ese ID.")
        return

    name = input("Nombre (requerido): ").strip()
    if not name:
        print("El nombre no puede estar vacío.")
        return

    email = input("Email: ").strip() or None
    phone = input("Teléfono: ").strip() or None
    address = input("Dirección: ").strip() or None
    tax_id = input("CUIT / Tax ID: ").strip() or None

    customer = Customer(
        id=customer_id,
        name=name,
        email=email,
        phone=phone,
        address=address,
        tax_id=tax_id,
    )

    customers.add_customer(customer)


def handle_search_customer(customers: CustomerManager) -> None:
    query = input("Nombre a buscar: ").strip()
    if not query:
        print("La búsqueda no puede estar vacía.")
        return

    results = customers.search_by_name(query)

    if not results:
        print("No se encontraron clientes.")
        return

    print("\n--- RESULTADOS ---")
    for customer in results:
        print(
            f"ID: {customer.id} | "
            f"Name: {customer.name} | "
            f"Email: {customer.email or '-'} | "
            f"Phone: {customer.phone or '-'} | "
            f"Tax ID: {customer.tax_id or '-'}"
        )


def handle_delete_customer(customers: CustomerManager) -> None:
    try:
        customer_id = int(input("ID del cliente a eliminar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    customers.delete_customer(customer_id)