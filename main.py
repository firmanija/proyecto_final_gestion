from product import Product
from employee import Employee
from sale import Sale
from inventory import Inventory
from datetime import datetime
from supplier import Supllier, SalesRepresentative

# Create Sales Representative por suppliers
rep1=SalesRepresentative(name="Carlos Perez", contact_info="carlos@yourbrand.com")

#Create Supplier
supplier1=Supllier(
    id=1,
    company_name="Empresa ejemplo",
    fantasy_name="Nombre de la marca X",
    representative=rep1,
    tax_info="Cuit 20-12345678-9"
)



# Create products
product1 = Product(1, "Shirt", "Cotton shirt", 20.0, 50)
product2 = Product(2, "Pants", "Denim pants", 35.0, 30)

# Simulation of transaction
supplier1.record_transaction(product1.name,10)
supplier1.record_transaction(product1.name,5)

supplier1.display_supplier_info()


# Create inventory and add products
inventory = Inventory()
inventory.add_product(product1)
inventory.add_product(product2)


# Add to stock 
inventory.add_stock(1, 20)  
inventory.add_stock(2, 10)  

# Remove stock
inventory.remove_stock(1, 5)

# List products
inventory.list_products()

# Create employee
employee1 = Employee(
    id=1, 
    name="John", 
    salary=1500, 
    hourly_wage=15,  
    position="Sales Rep",  
    start_date=datetime(2023, 1, 15)  
)

# Show employee info
employee1.display_info()




# Make a sale
sale1 = Sale(1, product1, employee1, 2)

# Show total sale
print(f"Total sale: ${sale1.total}")
