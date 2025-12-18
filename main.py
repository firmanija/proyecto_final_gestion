from product import Product
from employee import Employee
from sale import Sale
from inventory import Inventory
from datetime import datetime
from supplier import Supllier, SalesRepresentative
from petty_cash import Pettycash


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

def add_product_item():
   #user enters new item
   id=int(input("Enter product ID:"))
   name=input("Enter item name:")
   description=input("Enter description for item:")
   price=float(input("Enter price for item:"))
   stock=int(input("Enter item stock in units:"))

   unique_code=input("Enter unique code for item (leave blank if not applicable):")
   brand_code=input("Enter unique code for brand (leave blank if not applicable):")
   supplier_code=input("Enter unique code for supplier (leave blank if not applicable):")
   group_code=input("Enter group code (shirts, pants, shorts, etc) (leave blank if not applicable):")
   material=input("Enter type of fabric for item (leave blank if not applicable):")
   cost_price=input("Enter cost price for item (leave blank if not applicable):")
   includes_tax = input("Does it include taxes? (yes or no): ").strip().lower() == 'yes' 
   entry_date=datetime.now()
   season=input("Enter season for item (summer, winter, etc)(leave blank if not applicable): ")
   price_list_credit=input("Enter price for credit sales (leave blank if not applicable)")
   price_list_cash=input("Enter price for cash sales (leave blank if not applicable)")
   sizes_input = input("Enter sizes (comma-separated, e.g., S,M,L, leave blank if not applicable): ")
   sizes = [size.strip() for size in sizes_input.split(",")] if sizes_input else []

   # convert costs and final prices to a float
   cost_price=float(cost_price) if cost_price else None
   price_list_credit=float(price_list_credit) if price_list_credit else None
   price_list_cash=float(price_list_cash) if price_list_cash else None


   
   #Create an instance of the product
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
        sizes=sizes
    )
 
   product_item.display_info()



  #Petty cash
def manage_petty_cash():
   petty_cash= Pettycash()
   employee_id=input("Enter employee id for cash register opening:")
   inital_amount=float(input("Enter the inital amount left from previous day"))
   petty_cash.open_cash_register(employee_id, inital_amount)

   while True:
      action=input("Would you like to (1) add expense, (2) list transactions, "
      "(3) modify transaction, (4) delete transaction, (5) print closing report, "
      "(6) close register, or (7) exit? ").strip()

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
      
      elif action == '7':
         print("Exciting petty cash managment.")
         break
      else:
         print("Invalid option. Please try again")

       
if __name__=="__main__":
   manage_petty_cash()



def main ():
 if __name__== "__main__":
    
     while True:
        add_more = input("Do you want to add another product item? (yes or no): ").strip().lower()
        if add_more == 'yes':
            add_product_item()  
        elif add_more == 'no':
            print("Exiting the program.")
            break
        else:
            print("Invalid input, please enter 'yes' or 'no'.")



