from datetime import datetime

class Transaction:
    def __init__(self, employee_id, amount, description):
        self.employee_id=employee_id
        self.amount=amount
        self.description=description
        self.date=datetime.now()

class Pettycash:
    def __init__(self):
        self.balance=0.0
        self.transactions=[]

    def open_cash_register(self, employee_id, intial_amount):
        """Open cash register with the previous day's balance."""
        self.balance += intial_amount
        self.transactions.append(Transaction(employee_id, intial_amount, "Opening cash balance"))
        print(f"Petty cash box open with an initial balance of: ${intial_amount:.2f}")

    def add_expense(self, employee_id, amount, description):
         """Add an expense to petty cash register."""
         if amount> self.balance:
            print("There is not enough money to cover this expense.")
         self.balance -= amount
         self.transactions.append(Transaction(employee_id, -amount, description))
         print(f"The expense of  ${amount:.2f} has been registered for : {description}")
    
    def list_transactions(self):
          """List all petty cash transactions."""
          for trans in self.transactions:
              print("{trans.date}: {trans.description} (${trans.amount:.2f}), Made by employee ID: {trans.employee_id}")

    def modify_transaction(self, index, new_amount, new_description):
          """Modifies a specific transaction."""
          if index < 0 or index >= len(self.transactions):
              print("Invalid transaction.")
              return
          
          old_transaction=self.transactions[index]
          self.balance -= old_transaction.amount 
          self.balance += new_amount
          self.transactions[index]=  Transaction(old_transaction.employee_id, new_amount, new_description)
          print("Transaction has been modified.")
    
    def delete_transaction(self,index):
        """Deletes a specify transaction ."""
        if index < 0 or index >= len(self.transactions):
            print("Invalid transaction.")
            return
        
        transaction= self.transactions.pop(index)
        self.balance -= transaction.amount
        print(f"Deleted transaction: {transaction.description} (${transaction.amount:.2f})")

    def print_closing_report(self):
        """Print fiscal closing report (simulated)."""
        print("Fiscal day-end Z")
        print(f"Total balance of pettycash: ${self.balance:.2f}")
        print("Transactions:")
        self.list_transactions()

    def close_cash_register(self):
        """Close the petty cash register."""
        print("Petty cash closing completed.")
        print(f"Final balance: ${self.balance:.2f}")
        self.transaction=[]
