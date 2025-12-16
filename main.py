from product import Product
from employee import Employee
from supplier import Supplier
from sale import Sale

# Create products
product1 = Product(1, "Shirt", "Cotton shirt", 20.0, 50)

# Create employee
employee1 = Employee(1, "John", 1500)

# Create supplier
supplier1 = Supplier(1, "Supplier A", "contact@supplierA.com")

# Make a sale
sale1 = Sale(1, product1, employee1, 2)

# Show total sale
print(f"Total sale: ${sale1.total}")
