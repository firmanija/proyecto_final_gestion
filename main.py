from product import Product
from employee import Employee
from sale import Sale
from inventory import Inventory
from datetime import datetime
from supplier import Supllier, SalesRepresentative
from petty_cash import Pettycash
from data_managment import save_products_to_json, load_products_from_json
from transfer import Transfer
from sales_analysis import SalesAnalysis

# Create Sales Representative for suppliers
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
sales_analysis = SalesAnalysis()
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
sales_analysis.record_sale(product1.name, 2) 

# Show total sale
print(f"Total sale: ${sale1.total}")
sales_analysis = SalesAnalysis() 

 #Create an instance of the product
def add_product_item():
    # Input a new product or item
    id = int(input("Enter product ID: "))
    name = input("Enter product name: ")
    description = input("Enter product description: ")
    price = float(input("Enter product price: "))
    stock = int(input("Enter product stock: "))
    unique_code = input("Enter unique code for the item (leave blank if not applicable): ")
    brand_code = input("Enter unique code for the brand (leave blank if not applicable): ")
    supplier_code = input("Enter unique code for the supplier (leave blank if not applicable): ")
    group_code = input("Enter group code (e.g., shirts, pants) (leave blank if not applicable): ")
    material = input("Enter type of material (leave blank if not applicable): ")
    cost_price = input("Enter cost price (leave blank if not applicable): ")
    includes_tax = input("Does it include taxes? (yes or no): ").strip().lower() == 'yes'
    entry_date = datetime.now()  
    season = input("Enter the season (e.g., Summer, Winter) (leave blank if not applicable): ")
    price_list_credit = input("Enter the price for credit sales (leave blank if not applicable): ")
    price_list_cash = input("Enter the price for cash sales (leave blank if not applicable): ")
    channel = input("Enter the sales channel (e.g., retail, e-commerce, wholesale): ")

    # Convert prices and cost to a float
    cost_price = float(cost_price) if cost_price else None
    price_list_credit = float(price_list_credit) if price_list_credit else None
    price_list_cash = float(price_list_cash) if price_list_cash else None

    # Create an instance of the product
    product_item = Product(
        id=id,
        name=name,
        description=description,
        price=price,
        stock=stock,
        unique_code=unique_code if unique_code else None,
        brand_code=brand_code if brand_code else None,
        supplier_code=supplier_code if supplier_code else None,
        group_code=group_code if group_code else None,
        material=material if material else None,
        cost_price=cost_price,
        includes_tax=includes_tax,
        entry_date=entry_date,
        season=season if season else None,
        price_list_credit=price_list_credit,
        price_list_cash=price_list_cash,
        channel=channel if channel else None
    )
    product_item.display_info()
    return product_item 
 
def manage_inventory_transfers(inventory):
    while True:
        action = input("Would you like to (1) transfer product, (2) list transfers, or (3) exit? ").strip()
        
        if action == '1':
            product_id = int(input("Enter product ID to transfer: "))
            quantity = int(input("Enter quantity to transfer: "))
            from_location = input("Enter from location: ")
            to_location = input("Enter to location: ")
            inventory.transfer_product(product_id, quantity, from_location, to_location)
        
        elif action == '2':
            inventory.list_transfers()
        
        elif action == '3':
            print("Exiting inventory transfers management.")
            break
        
        else:
            print("Invalid option, please try again.")

 
def manage_returns(inventory):
    while True:
        return_action = input("Would you like to (1) process return, or (2) exit? ").strip()
        
        if return_action == '1':
            product_id = int(input("Enter product ID to return: "))
            quantity = int(input("Enter quantity to return: "))
            product = inventory.get_product(product_id)
            if product:
                product.process_return(quantity)  
            else:
                print("Product not found in inventory.")
        
        elif return_action == '2':
            print("Exiting returns management.")
            break
        
        else:
            print("Invalid option, please try again.")

def show_sales_analysis(sales_analysis):
    """Show Sales Analysis."""
    print(f"Most Sold Product: {sales_analysis.most_sold_product()}")
    print(f"Least Sold Product: {sales_analysis.least_sold_product()}")

def main():
    products = load_products_from_json()
    sales_analysis = SalesAnalysis()
    while True:
        action = input("Choose an action: (1) Add Product, (2) View Products,(3) Manage Returns, (4) Make Sale, (5) Exit: ").strip()
        if action == '1':
            product_item = add_product_item() 
            products.append(product_item)
            sales_analysis.record_sale(product_item.name, product_item.stock)
        
        elif action == '2':
           for product in products:
                product.display_info()

        elif action == '3':
          manage_returns(inventory) 

        elif action == '4':
           product_id = int(input("Enter product ID to sell: "))
           quantity = int(input("Enter quantity to sell: "))
           payment_method_type = input("Enter payment method (1 for Credit Card, 2 for Cash): ").strip()
           payment_method = credit_card if payment_method_type == '1' else cash
            
           product = inventory.get_product(product_id)
           if product and quantity <= product.stock:
                sale_id = len(sales_analysis.sales_data) + 1

                sale = Sale(sale_id, product, employee1, quantity, payment_method)
                sales_analysis.record_sale(product.name, quantity)
                payment_method.record_payment(sale.total)  
                print(f"Sale recorded: {quantity} x {product.name} sold. Total: ${sale.total:.2f}")
           else:
                print("Product not found or insufficient stock.")
        

        elif action == '5':
            save_products_to_json(products)
            show_sales_analysis(sales_analysis)  # Muestra el análisis de ventas
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")
  


def manage_petty_cash():
   petty_cash= Pettycash()
   employee_id=input("Enter employee id for cash register opening:")
   inital_amount=float(input("Enter the inital amount left from previous day"))
   petty_cash.open_cash_register(employee_id, inital_amount)

   while True:
      action=input("Would you like to (1) add expense, (2) list transactions, "
      "(3) modify transaction, (4) delete transaction, (5) print closing report, "
      "(6) close register,(7) manage returns,  or (8) exit? ").strip()

      if action =='1':
         employee_id=input("Enter your employee ID:")
         amount=float(input("Enter the expense amount:"))
         description=input("Enter the expense description:")
         petty_cash.add_expense(employee_id, amount, description)
    
      elif action == '2':
         petty_cash.list_transactions()

      elif action == '3':
         index=int(input("Enter the index of the transaction to modify:"))
         new_amount=float(input("Enter new amount:"))
         new_description = input("Enter the new description: ")
         petty_cash.modify_transaction(index, new_amount,new_description)
      
      elif action == '4':
         index=int(input("Enter the index of transaction to delete:"))
         petty_cash.delete_transaction(index)

      elif action == '5':
         petty_cash.print_closing_report()

      elif action == '6':
         petty_cash.close_cash_register()
         break
      elif action =='7':
           manage_returns(inventory)
      
      elif action == '8':
         print("Exciting petty cash managment.")
         break
      else:
         print("Invalid option. Please try again")

       



if __name__ == "__main__":
   main()
   manage_petty_cash()
   products = load_products_from_json()
   manage_inventory_transfers(inventory)
   sales_analysis = SalesAnalysis()
   credit_card = PaymentMethod("Tarjeta de Crédito")
    cash = PaymentMethod("Efectivo")


           
   

