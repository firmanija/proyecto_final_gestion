from datetime import datetime

class Transaction:
    def __init__(self,product_name,quantity,date):
        self.product_name=product_name
        self.quantity=quantity
        self.date=date
    
class SalesRepresentative:
    def __init__(self,name,contact_info):
        self.name=name
        self.contact_info=contact_info

class Supllier:
    def __init__(self, id, company_name, fantasy_name, representative, tax_info):
        self.id=id
        self.company_name=company_name
        self.fantasy_name=fantasy_name
        self.representative=representative
        self.tax_info=tax_info
        self.transaction_history=[]
        self.first_transaction_date=None
        self.last_order=None

    def record_transaction(self, product_name, quantity):
        order_date= datetime.now()
        transaction= Transaction(product_name, quantity, order_date,)
        self.transaction_history.append(transaction)

        if not self.first_transaction_date:
            self.first_transaction_date= order_date

        self.last_order= transaction

    def display_supplier_info(self):
        print(f"Supplier ID: {self.id}, Company: {self.company_name}, "
              f"Fantasy Name: {self.fantasy_name}, "
              f"Representative: {self.representative.name}, "
              f"Contact: {self.representative.contact_info}, "
              f"Tax Info: {self.tax_info}")
        
        print("Transaction History:")
        for trans in self.transaction_history:
            print(f" - {trans.date} - {trans.product_name} - Quantity: {trans.quantity}")

        if self.last_order:
            print(F"Last Order:{self.last_order.product_name} - Quantity:{self.last_order.quantity} on {self.last_order.date}")
            